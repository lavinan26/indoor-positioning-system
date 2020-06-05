# indoor-positioning-system
An IoT application to locate an ESP32 device inside a building with beacons using BLE (Bluetooth Low Energy) signals. 

![Image](system_architecture.png)

## Usage

Deploy node-red App

1. start the node-red app in local machine or on remote host
```bash 
node-red
```
2. Go to http://localhost:1880/ or http://{publicIP}:1880/ for remote host
3. Import the flow "node_red_web_app.json" and deploy
4. Go to http://localhost:1880/ui

To start the python backend

```bash
python App.py
```
