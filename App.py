import time
import paho.mqtt.client as paho
import csv
import json
import numpy as np
import pickle
from sklearn.svm import SVC
broker="mqtt.eclipse.org"
#define callback
MACAddresses = {'f0:ec:af:cf:6c:e1':1,'c9:a6:4d:9b:c0:8c':2,'c2:b6:6e:70:fa:f7':3,'d9:5f:f5:4f:10:89':4,'c4:52:32:5c:31:e7':5,'e9:3c:4a:34:13:fb':6,'ed:61:e4:e8:22:30':7,'ea:01:26:75:a4:c3':8,'d0:4e:10:2e:cb:84':9,'e4:e0:0a:ae:fd:e2':10,'fa:35:76:56:6f:e3':11,'d5:b7:dc:69:ca:ae':12,'ca:81:7a:d7:55:49':13,'e7:2b:ea:2f:95:c5':14,'d4:32:fc:b5:f0:b5':15}
coordinates = {'1':[149,117],'2':[75,166],'3':[59,142],'4':[118,157],'5':[187,148],'6':[211,158],'7':[171,176],'8':[294,118],'9':[278,157],'10':[221,151],'11':[200,230],'13':[170,200],'14':[150,200],'15':[180,230],'16':[200,250],'17':[230,250],'18':[250,280],'19':[280,280],'20':[160,190],'21':[224,184],'22':[250,160],'23':[270,230]}
svclassifier = pickle.load(open('svclassifier_2.pickle','rb'))

def on_message(client, userdata, message):
    noSignal = 1
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))
    msg = json.loads(str(message.payload.decode("utf-8")))
    print(json.dumps(msg))
    signal = {"f0:ec:af:cf:6c:e1":-200,"c9:a6:4d:9b:c0:8c":-200,"c2:b6:6e:70:fa:f7":-200,"d9:5f:f5:4f:10:89":-200,"c4:52:32:5c:31:e7":-200,"e9:3c:4a:34:13:fb":-200,"ed:61:e4:e8:22:30":-200,"ea:01:26:75:a4:c3":-200,"d0:4e:10:2e:cb:84":-200,"e4:e0:0a:ae:fd:e2":-200,"fa:35:76:56:6f:e3":-200,"d5:b7:dc:69:ca:ae":-200,"ca:81:7a:d7:55:49":-200,"e7:2b:ea:2f:95:c5":-200,"d4:32:fc:b5:f0:b5":-200}
    print(json.dumps(signal))
    input_data = np.ones((1,15))*(-200)
    for i in MACAddresses:
        if (i in msg):
            input_data[0,MACAddresses[i]-1]=msg[i]
            signal[i] = msg[i]
            noSignal = 0
    result = svclassifier.predict(input_data)
    print(result)
    prob = svclassifier.predict_proba(input_data).max()
    response = {"prediction":result.item(),"probability":round(prob,2)*100,"coordinates":coordinates[str(result.item())],"signals":signal,"nothing":noSignal}
    print(json.dumps(response))
    client.publish("BLE_la",json.dumps(response))
    print("done")
    

client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("BLE_lavin")#subscribe
time.sleep(200)
client.disconnect() #disconnect
client.loop_stop() #stop loop