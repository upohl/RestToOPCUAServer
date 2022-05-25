# RestToOPCUAServer
Converts a Rest Get Call to an OPCUA Server

## Requirements 
Python 3.7 

## Install 
git clone https://github.com/upohl/RestToOPCUAServer.git
cd RestToOPCUAServer
pip install requirements.txt

## Examples 
### Starts OPC UA Server on default port 4840 and calls ISS Position (http://api.open-notify.org/iss-now.json)
python resttoopcuaserver.py

### Starts OPC UA Server on port 4841 and calls ISS Position (http://api.open-notify.org/iss-now.json)
python resttoopcuaserver.py -p 4841

### Starts OPC UA Server on default port 4840 and delimter ":"
python resttoopcuaserver.py -d :

### Starts OPC UA Server on default port 4840 and rest url https://api.coincap.io/v2/assets/bitcoin
python resttoopcuaserver.py -u https://api.coincap.io/v2/assets/bitcoin

### Starts OPC UA Server on port 4841, delimter : and rest url https://api.coincap.io/v2/assets/bitcoin
python resttoopcuaserver.py -p 4841 -d : -u https://api.coincap.io/v2/assets/bitcoin