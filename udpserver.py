# --*-- coding:utf-8 -*-
import socket
from sqlapi import sql_conn, sql_close
# 
# length(2) ver(1) type(1)   sn(16)      magicnum(4)
# |--------|----|----|----------------|----------------|

PACKET_LENGTH_MIN = 24

SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 10000

PACKET_TYPE_REGISTER = 0x1
PACKET_TYPE_REGISTER_RESPONSE = 0x2
PACKET_TYPE_LOCATION = 0x3

DEBUG_LEVEL_CLOSE = 0
DEBUG_LEVEL_ERROR = 0x1
DEBUG_LEVEL_INFO = 0x2
DEBUG_LEVEL = DEBUG_LEVEL_INFO | DEBUG_LEVEL_ERROR


def parse_register_packet(str):
	ret = 0
	sn = None

	for index in range(len(str)):
		if str[index] != '#':
			sn = str[index:]
			break

	if sn == None:
		if DEBUG_LEVEL & DEBUG_LEVEL_ERROR:
			print "sn(%s) is invalid" % str
		ret = 1
		return ret

	#sql_conn(conn, cur)

	return ret


def parse_location_packet(data):
	ret = 0

	return ret


def parse_packet(data):
	ret = 0

	data_len = len(data)
	if data_len < PACKET_LENGTH_MIN:
		ret = 1
		return ret

	length = data[0:2]
	if length != data_len:
		ret = 2
		return ret

	version = data[2:3]
	type = data[3:4]
	sn = data[4:20]
	magicnum = data[20:24]

	if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		print "Recv packet from sn=", sn, " which type=", type, " version=", version, " magicnum=", magicnum

	type = int(type, 16)
	if (type == PACKET_TYPE_REGISTER) or (parse_register_packet(sn) != 0):
		ret = 3
	elif (type == PACKET_TYPE_LOCATION) or (parse_location_packet(data) != 0):
		ret = 3
	else:
		ret = 3

	return ret


def main():	
	address = (SERVER_IP_ADDRESS, SERVER_PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(address)
	print "Socket init succeed, waiting for recv packet..."

	conn = None
	cur = None
	(conn, cur) = sql_conn()
	cur.execute('select * from InterActionTransTable')
	for row in cur:
		print row[0], row[1], row[2]
	sql_close(conn, cur)


	while True:
		err = 0
		data, addr = sock.recvfrom(4096)

		if not data:
			print "Has not recvived data."
			continue
		print "Received(", len(data), "):", data, "from", addr

		err = parse_packet(data)
		if (err != 0):
			if DEBUG_LEVEL & DEBUG_LEVEL_ERROR:
				print "Parse packet error:", err
			continue
	sock.close()


if __name__ == "__main__":
	main()	
