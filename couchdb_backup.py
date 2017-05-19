# -*- coding: utf8 -*-
import requests, json, os, sys

db_name = []
id_name = []
def JSON_Get_all_database(db_url=''):
	tmp_url=db_url+'/'+'_all_dbs'
#	print(url)
#	rev = requests.get(tmp_url, auth=(username,password))
#	print(rev.text)
	tmp_text = Request_Get(tmp_url)
	print(tmp_text)
#	tmp_data = Separate_String(tmp_text)
	for each_db in tmp_text:
		db_name.append(each_db)
		print('\n\n'+each_db)
		JSON_Get_URL_all_docs(each_db)
#		JSON_Get_Json_Format(each_db, id_name)
#		id_name = []

def JSON_Get_URL_all_docs(tmp_db_name):
	tmp_url=db_url+'/'+tmp_db_name+'/'+"_all_docs"
	print(tmp_url)
#	rev = requests.get(tmp_url, auth=(username,password))
#	tmp_json_obj = json.loads(rev.text)
	json_obj = Request_Get(tmp_url)
	print(json_obj)
#	print("")
#	print(json_obj['rows'])
	JSON_Get_rows(json_obj['total_rows'], json_obj)
	print('\n\n'+tmp_db_name+'\n')
	print(id_name)
	JSON_Get_Json_Format(tmp_db_name, id_name)

def JSON_Get_rows(docs_num, tmp_json_obj=''):
#	print("")
#	print(tmp_json_obj)
#	print("")
#	print(docs_num)
	while docs_num > 0:
		doc_id = tmp_json_obj['rows'][docs_num-1]['id']
#		print(doc_id)
		doc_id_modified = JSON_Modify_Id_Character(doc_id) 
#		print(doc_id_modified)
		id_name.append(doc_id_modified)
		docs_num -= 1

def JSON_Modify_Id_Character(doc_id):
	doc_id_modified = doc_id.replace('/', '%2F')
	return doc_id_modified

def JSON_Get_Json_Format(db_name, tmp_doc_id):
	for each_id in tmp_doc_id:
		tmp_url = db_url+'/'+db_name+'/'+each_id
#		print(tmp_url)
#		rev = requests.get(tmp_url, auth=(username,password))
#		doc_json_format = rev.text
		doc_json_format = Request_Get(tmp_url)
#		print(doc_json_format)
		Json_Save_Json_File(doc_json_format, each_id)
	del id_name[:]

def Json_Save_Json_File(tmp_json_format='', tmp_doc_id=''):
	json = str(tmp_json_format)
	dir_path = 'CouchDB_json'
	file_path = dir_path+'/'+tmp_doc_id+'.json'
	print(file_path)
	file=open(file_path,'wb')
	file.write(json.strip().encode('utf-8'))
	file.close()

def Get_Local_Hostname():
	str1 = os.popen('hostname').read()
	hostname = str1[0:-1]

def Separate_String(tmp_data):
	tmp_data = tmp_data.replace('"','')
	tmp_data = tmp_data.replace('[','')
	tmp_data = tmp_data.replace(']','')
	tmp_data = tmp_data.replace('\n','')
#	print(tmp_data)
	tmp_data = tmp_data.split(',')
#	print(tmp_data)
	return tmp_data

def Request_Get(URL):
	if '127.0.0.1' in db_url:
		rev = requests.get(URL)	
	else:
		rev = requests.get(URL, auth=(username,password))
	tmp_json_obj = json.loads(rev.text)
	return tmp_json_obj

DEBUG = 0
if len(sys.argv) < 2:
	print('Usage : python3 couchdb_backup.py [dump|load|merge] [CouchDB URL]')
	sys.exit()

username = '4fa75cd1-58c9-40f8-b564-f0ea711bd506-bluemix'
password = '9490c5b340b894b4db5f02b357cf59bf1a6fec84543e2080bcb1049cd2d4a4f5'

cmd = sys.argv[1]
db_url = sys.argv[2]
if DEBUG == 1:
	print(cmd)
	print(db_url)
	print(username)
	print(password)

if cmd == 'dump':
	print('dumping...')
	JSON_Get_all_database(db_url)
#	print(id_name)
#	print(db_name)
elif cmd == 'load':
	print('loading...')
	JSON_Get_all_database(db_url)
elif cmd == 'merge':
	JSON_Get_URL_all_docs('nodered')
	print('')
	JSON_Get_URL_all_docs('humix')
else:
	print('Command is dump or load.\n"dump" from CouchDB or "load" into CouchDB.')
