"""Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.    
"""
# Created By  : Uwe Pohlmann (https://github.com/upohl)
# Created Date: 2022/05/25
# version ='0.1'

import logging
import asyncio
import sys, getopt
import re

sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server.user_managers import CertificateUserManager
import requests
from requests.auth import HTTPBasicAuth
import json
import flatdict
from os.path import exists
from datetime import datetime




"""Recursively fetch primitives (int, float, bool) from nested JSON and adds as key/value pair to flat dictionary"""
def json_extract(obj):
    mydict = {}
  
    def extract(obj, mydict):
        """Recursively search for values of primitives in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, mydict)
                elif isinstance(v, (int, float, bool, str)):
                    mydict[k] = v
        elif isinstance(obj, list):
            for item in obj:
                extract(item, mydict)
        return mydict

    values = extract(obj, mydict)
    return values



@uamethod
def func(parent, value):
    return value * 2

async def write_variable_value(variable,newvalue,_logger=None):
    if _logger is not None:
        _logger.info('Set value of %s to %.1f', variable, newvalue)
    await variable.write_value(newvalue)

async def main():
   port = 4840
   url = "http://api.open-notify.org/iss-now.json"
   delimiter = '.'
   cycle = 1
   username = ''
   password = ''

   _logger = logging.getLogger('asyncua')

   try:
        opts, args = getopt.getopt(sys.argv[1:],"p:u:d:c:n:m:",["port=","url=","delimiter=","cycle=","username=","password="])
   except getopt.GetoptError as err:
        print("resttoopcuaserver.py -p <port> -u <url> -d <delimter char> -c <seconds> -n <username> -m <password>")
        sys.exit(2)
   for o, a in opts:
       if  o in ("-p", "--port"):
           port = a
           _logger.info('Port: '+port)
       if  o in ("-u", "--url"):
           url = a
           _logger.info('Url: '+url)
       if  o in ("-d", "--delimiter"):
           delimiter = a
           _logger.info('delimiter: '+delimiter)
       if  o in ("-c", "--cycle"):
           cycle = int(a)
           _logger.info('cycle in seconds: '+str(cycle))
       if  o in ("-n", "--username"):
           username = str(a)
           _logger.info('username: '+username)
       if  o in ("-m", "--password"):
           password = str(a)
           _logger.info('password: '+'XZY####') 


   # setup our server
  
   server = Server()
  
   server.set_endpoint('opc.tcp://0.0.0.0:{}/freeopcua/server/'.format(port))
    # setup our own namespace, not really necessary but should as spec




   # load server certificate and private key. This enables endpoints
   # with signing and encryption.
   await server.init()


   if exists("certificate.der") and exists("key.pem"):
       await server.load_certificate("certificate.der")
       await server.load_private_key("key.pem")
       
       server.set_security_IDs(["Anonymous", "Basic256Sha256", "Username"])
       server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,ua.SecurityPolicyType.NoSecurity])
   else:
       server.set_security_policy([ua.SecurityPolicyType.NoSecurity])   
   uri = 'urn:localhost:freeopcua:server'.format(port)
   idx = await server.register_namespace(uri)
   subject=str(server.certificate.subject)
   m = re.search('CN=([^,]+)', subject)
   m.group(1)
   #now = 
   urn =  m.group(1)

   await server.set_build_info(urn,"My Company","RestToOPCUA Server","v0.1","",datetime.now())

   m = re.search('(.*)/', url)
   await server.set_application_uri(m.group(0));

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root

   #add root node
   root = await server.nodes.objects.add_object(idx, 'Root')
   try:
       if len(username) != 0 and len(password) != 0:
           _logger.info('Try secure request:')
           response = requests.get(url,auth=HTTPBasicAuth(username, password))
       else:  
           response = requests.get(url)
       # let only 200 OK pass     
       if response.status_code != 200:
           _logger.info('Failed request:' + str(response.status_code) )
           sys.exit(2)
       else:
           resp_object = json.loads(response.text)

       primitives = flatdict.FlatDict(resp_object, delimiter=delimiter)


       # primitives = json_extract(resp_object)
       opcuaTree = {}
       # add url as variable
       opcuaTree[url] = await root.add_variable(idx, 'url', url)
       for k, v in primitives.items():
        opcuaTree[k] = await root.add_variable(idx, k, v)

   except requests.exceptions.Timeout:
       # Maybe set up for a retry, or continue in a retry loop
       _logger.info('Timeout for '+url)
   except requests.exceptions.TooManyRedirects:
       # Tell the user their URL was bad and try a different one
       _logger.info('TooManyRedirects for '+url)
   except requests.exceptions.RequestException as e:
       # catastrophic error. bail.
       _logger.info('catastrophic error. bail. for '+url)
       raise SystemExit(e)

   
   _logger.info('Starting server!')
   async with server:
       while True:
           await asyncio.sleep(cycle)
           if len(username) != 0 and len(password) != 0:
               _logger.info('Try secure request:')
               response = requests.get(url,auth=HTTPBasicAuth(username, password))
           else:  
               response = requests.get(url)
           # let only 200 OK pass     
           if response.status_code != 200:
               _logger.info('Failed request:'+ str(response.status_code) )
               sys.exit(2)
           else:  
               resp_object = json.loads(response.text)
           # primitives = json_extract(resp_object)
           primitives = flatdict.FlatDict(resp_object, delimiter=delimiter)
           for k, v in primitives.items():
               await opcuaTree[k].write_value(v)
 
            


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
