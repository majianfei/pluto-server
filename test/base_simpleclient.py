# coding:utf8

import time

from socket import AF_INET, SOCK_STREAM, socket
from thread import start_new
import struct, json
import sys
import time

TOTAL = 1  # 总客户端数

HEAD_LEN = 8

global_data = ""

def sendData(command_id, sub_id, data):
	json_data = json.dumps(data)
	length = HEAD_LEN + len(json_data)

	data = struct.pack('!ihh', length, command_id, sub_id)
	senddata = data + json_data
	print "==============>",len(senddata)
	return senddata


def resolveRecvdata(idx):
	global global_data

	#print "data",len(global_data)
	
	if len(global_data) < HEAD_LEN:
		#print "error head short than 8:",len(global_data)
		return
		

	length, command, reverse = struct.unpack('!ihh', global_data[0:HEAD_LEN])
	print "receive",length,command,reverse
	if length > 1024 or length < HEAD_LEN:
		print "error receive length:",length
		return
	if len(global_data) < length:
		print "error length is to short:",len(global_data)
		return
	data = global_data[HEAD_LEN:length]
	
	print "data2:",length,"-- ", len(data)

	global_data = global_data[length:]
	
	print "json", data
	#data = data[0:len(data)-1]
	#print "json", data
	#data = '{"result":"yes","lv":1}'
	
	
	
	result = json.loads(data)
	
	print "---",result
	#print "result",result['id']
	#print "lv",result['name']
	
	resolveRecvdata(idx)


def receiveMessage(connection):
	global global_data

	while 1:
		#for idx, connection in enumerate(connections):
		idx = 0
		print "idx=========>",idx
		message = connection.recv(1024)
		print "idx=========>",idx
		global_data += message
		resolveRecvdata(idx)
		#time.sleep(0.2)

HOST = '127.0.0.1'
PORT = 5000
ADDR = (HOST, PORT)

if __name__ == "__main__":
	args = sys.argv
	servername = None
	config = None

	client_list = []

	for i in xrange(TOTAL):
		client = socket(AF_INET, SOCK_STREAM)
		client.connect(ADDR)
		#client.setblocking(0)
		client_list.append(client)

	start_new(receiveMessage, (client_list[0],))
	
	#print "now create"
	#for i in xrange(TOTAL):
	#	data = {"id":100+i, "n":"h"}
	#	client.sendall(sendData(1, 1, data))  # 登陆角色
	#time.sleep(3)

	print "now login"
	for i in xrange(TOTAL):
		data = {"id":101+i, "n":"h"}
		client.sendall(sendData(1, 2, data))  # 登陆角色
	time.sleep(3)
	
	print "now talk"
	for i in xrange(TOTAL):
		data = {"msg":"hello1111"}
		client.sendall(sendData(3, 1, data))  # 聊天
	time.sleep(3)

	print "now over"
	#print "333333"
	#client.sendall(sendData(1,99, data))
	#time.sleep(1)

	while(1):
		time.sleep(0.1)
