#coding=utf-8
import requests
import json
import os


#######flow#######
##1. get local hostname and rev
##2. rewrite in git download json
##3. upload to couchDB
#######flow#######

##veriable value##
file_flow = 'flow.json'
file_settings = 'settings.json'
file_credential = 'credential.json'
file_dl = 'design_library.json'
##veriable value##

def get_rev(node_name='null',hostname='none'):
    url = "http://127.0.0.1:5984/nodered/"+hostname+"%2F"+node_name
    rev = requests.get(url)
    json_obj = json.loads(rev.text)
    return json_obj['_rev']

def rewrite_id_rev(hostname='null',rev='null',file_name='null'):
    f=open(file_name,'r')
    new = 'new'+file_name
    fout=open(new,'w')
    r=f.read()
    f.close()
    json_obj = json.loads(r)
    json_obj['_id']=hostname+'/flow'
    json_obj['_rev']=rev
    outStr = json.dumps(json_obj, ensure_ascii = False) 
    fout.write(outStr.strip().encode('utf-8'))
    fout.close()

def upload_to_couchDB(node_name='null',hostname='null',file_name='null'):
    url = "http://127.0.0.1:5984/nodered/"+hostname+"%2F"+node_name
    new = 'new'+file_name
    file =open(new,'r')
    x=file.read()
    p=requests.put(url,x)
    print p.text
    file.close()
    
    
##1.1 get host name##
str1 = os.popen('hostname').read()
hostName = str1[0:-1]
##1.1 get host name##

##1.2 get rev##
flow_rev = get_rev('flow',hostName)
credential_rev = get_rev('credential',hostName)
settings_rev = get_rev('settings',hostName)
#design lib?#

##1.2 get rev##

##2. rewrite in git download json##
rewrite_id_rev(hostName,flow_rev,file_flow)
rewrite_id_rev(hostName,settings_rev,file_settings)
rewrite_id_rev(hostName,credential_rev,file_credential)
##2. rewrite in git download json##


##design library##
url = "http://127.0.0.1:5984/nodered/_design/library"
rev = requests.get(url)
json_obj = json.loads(rev.text)
dl_rev = json_obj['_rev']
f=open(file_dl,'r')
new = 'new'+file_dl
fout=open(new,'w')
r=f.read()
f.close()
json_obj = json.loads(r)
json_obj['_rev']=dl_rev
outStr = json.dumps(json_obj, ensure_ascii = False) 
fout.write(outStr.strip().encode('utf-8'))
fout.close()

file =open(new,'r')
x=file.read()
p=requests.put(url,x)
print p.text
file.close()

##design library##



##3. upload to couchDB##
upload_to_couchDB('flow',hostName,file_flow)
upload_to_couchDB('credential',hostName,file_credential)
upload_to_couchDB('settings',hostName,file_settings)
##3. upload to couchDB##







