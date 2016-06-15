# --*-- coding:utf-8 -*-
import socket
import struct
from sqlapi import sql_conn, sql_close
# 
# length(2) ver(1) type(1)   sn(16)      magicnum(4)
# |--------|----|----|----------------|----------------|

PACKET_LENGTH_MIN = 24
INSOLE_VERSION = 0x01
PACKET_MAGICNUM = 0xffffffff


SERVER_IP_ADDRESS = "192.168.1.12"
SERVER_PORT = 10000

PACKET_TYPE_REGISTER = 0x1
PACKET_TYPE_REGISTER_RESPONSE = 0x2
PACKET_TYPE_LOCATION = 0x3

INSOLE_STATE_NOTREGISTERED = 0x0
INSOLE_STATE_REGISTERED = 0x1


INSOLE_STATE_INDEX = 0x2

DEBUG_LEVEL_CLOSE = 0
DEBUG_LEVEL_ERROR = 0x1
DEBUG_LEVEL_INFO = 0x2
DEBUG_LEVEL = DEBUG_LEVEL_INFO | DEBUG_LEVEL_ERROR


def send_register_reply(errcode, sn, address):
	length = PACKET_LENGTH_MIN + 4

	if errcode == 0:
		state = INSOLE_STATE_REGISTERED
	else:
		state = INSOLE_STATE_NOTREGISTERED	

	if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		print "We will send sn=%s address=%s a register reply packet state=%d." % (sn, address, state)
	reply_packet = struct.pack("!H2b16s2I", length, INSOLE_VERSION, PACKET_TYPE_REGISTER_RESPONSE, sn, PACKET_MAGICNUM, state)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(reply_packet, address)
	s.close()



def parse_register_packet(str):
	ret = 0
	sn = None

	#for index in range(len(str)):
	#	if str[index] != '#':
	#		sn = str[index:]
	#		break
	sn = str

	if sn == None:
		if DEBUG_LEVEL & DEBUG_LEVEL_ERROR:
			print "sn(%s) is invalid." % str
		ret = 1
		return ret

	#if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		#print "sn is %s" % sn

	conn = None
	cur = None
	(conn, cur) = sql_conn()
	cur.execute('select * from insole_register_info where sn=%s', (sn))
	rows = cur.fetchall()

	if cur.rowcount == 0:
		if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
			print "insert a item into database where sn=%s." % (sn)
		cur.execute('insert into insole_register_info values(%s, %d)', (sn, INSOLE_STATE_REGISTERED))
		conn.commit()
	elif rows[0][INSOLE_STATE_INDEX] != INSOLE_STATE_REGISTERED:
		if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
			print "update a item to registered into database where sn=%s." % (sn)
		cur.execute('update insole_register_info set state = %d where sn = %s', (INSOLE_STATE_REGISTERED, sn))
		conn.commit()
	else:
		if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
			print "sn is %s register state is %d." % (sn, rows[0][INSOLE_STATE_INDEX])
		ret = 0
		return ret

	return ret


def parse_location_packet(data):
	ret = 0

	return ret


def parse_packet(data, address):
	ret = 0

	data_len = len(data)
	if data_len < PACKET_LENGTH_MIN:
		ret = 1
		return ret

	length, version, type, sn, magicnum = struct.unpack("!H2b16sI", data)
	if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		print "length:%d version:%d type:%d sn:%s magicnum:%x." % (length, version, type, sn, magicnum)

	#length = int(data[0:2], 16)	
	if length != data_len:
		ret = 2
		return ret

	#version = data[2:3]
	#type = data[3:4]
	#sn = data[4:20]
	#magicnum = data[20:24]

	#if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		#print "Recv packet from sn=", sn, " which type=", type, " version=", version, " magicnum=", magicnum

	#type = int(type, 16)
	if type == PACKET_TYPE_REGISTER:
		code = parse_register_packet(sn)
		send_register_reply(code, sn, address)
	elif type == PACKET_TYPE_LOCATION:
		code = parse_location_packet(data)
	else:
		ret = 3

	return ret


def main():	
	address = (SERVER_IP_ADDRESS, SERVER_PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(address)
	print "Socket init succeed, waiting for recv packet..."

	#conn = None
	#cur = None
	#(conn, cur) = sql_conn()
	#cur.execute('select * from InterActionTransTable')
	#for row in cur:
	#	print row[0], row[1], row[2]
	#sql_close(conn, cur)


	while True:
		err = 0
		data, addr = sock.recvfrom(4096)

		if not data:
			print "Has not recvived data."
			continue
		print "Received data_len:%d from %s." % (len(data), addr)

		err = parse_packet(data, addr)
		if (err != 0):
			if DEBUG_LEVEL & DEBUG_LEVEL_ERROR:
				print "Parse packet error:", err
			continue
		else:
			if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
				print "Parse packet succeed."	
	sock.close()


if __name__ == "__main__":
	main()	
