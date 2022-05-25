# RestToOPCUAServer
Converts a Rest API to an OPC UA Server that calls the REST API every second

## Requirements 

Python 3.7

UAExpert or any other OPC UA Client
https://www.unified-automation.com/de/produkte/entwicklerwerkzeuge/uaexpert.html

## Install 
`git clone https://github.com/upohl/RestToOPCUAServer.git`

`cd RestToOPCUAServer`

`pip install requirements.txt`

## Examples 
### Starts OPC UA Server on default port 4840 and calls default rest url (http://api.open-notify.org/iss-now.json) every second
`python resttoopcuaserver.py`

### Starts OPC UA Server on port 4841 and calls default rest url  (http://api.open-notify.org/iss-now.json) every second
`python resttoopcuaserver.py -p 4841`

### Starts OPC UA Server on default port 4840 and delimter ":"
`python resttoopcuaserver.py -d :`

### Starts OPC UA Server on default port 4840 and default rest url http://api.open-notify.org/iss-now.json every 5 seconds
`python resttoopcuaserver.py -c 5`

### Starts OPC UA Server on default port 4840 and rest url https://api.coincap.io/v2/assets/bitcoin
`python resttoopcuaserver.py -u https://api.coincap.io/v2/assets/bitcoin`

### Starts OPC UA Server on port 4841, delimter '.' and rest url https://api.coincap.io/v2/assets/bitcoin every 5 seconds
`python resttoopcuaserver.py -p 4841 -d . -u https://api.coincap.io/v2/assets/bitcoin -c 5`


## Screenshot of OPC UA CLient UAExpert Browsing the Example
![Screenshot of OPC UA CLient UAExpert Browsing the Example](/docs/images/screenshot1.png?raw=true "Screenshot")


## Public APIs
Currently GET API Calls without Authentication are supported without adapting the code
https://github.com/public-apis/public-apis
