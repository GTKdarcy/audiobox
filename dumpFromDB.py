#codinf=utf-8
import requests
import json
import os

def newOpen(filename='null'):
    str1 = os.popen('hostname').read()
    hostName = str1[0:-1]
    url = "http://127.0.0.1:5984/nodered/"+hostName+"%2F"+filename
    r=requests.get(url)        
    output=r.text
    F2 = filename+'.json'
    file=open(F2,'w')
    file.write(output.strip().encode('utf-8'))
    file.close()

newOpen('CouchDB_json/flow')
newOpen('CouchDB_json/settings')
newOpen('CouchDB_json/credential')


url = "http://127.0.0.1:5984/nodered/_design/library"
r=requests.get(url)        
output=r.text
F2 = 'CouchDB_json/design_library.json'
file=open(F2,'w')
file.write(output.strip().encode('utf-8'))
file.close()
