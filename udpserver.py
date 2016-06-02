# --*-- coding:utf-8 -*-
import socket
# 
#   length   ver type       sn(4)          magicnum
# |--------|----|----|----------------|----------------|

PACKET_LENGTH_MIN = 12

SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 10000

PACKET_TYPE_REGISTER = 0x1
PACKET_TYPE_REGISTER_RESPONSE = 0x2
PACKET_TYPE_LOCATION = 0x3

DEBUG_LEVEL_CLOSE = 0
DEBUG_LEVEL_ERROR = 0x1
DEBUG_LEVEL_INFO = 0x2
DEBUG_LEVEL = DEBUG_LEVEL_INFO | DEBUG_LEVEL_ERROR


def parse_register_packet(sn):
	ret = 0

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
	sn = data[4:8]
	magicnum = data[8:12]

	if DEBUG_LEVEL & DEBUG_LEVEL_INFO:
		print "Recv packet from sn=", sn, " which type=", type, " version=", version, " magicnum=", magicnum

	type = int(type, 16)
	if type == PACKET_TYPE_REGISTER:
		ret = parse_register_packet(sn)
	else if type == PACKET_TYPE_LOCATION:
		ret = parse_location_packet(data)
	else
		ret = 3

	return ret


def main():	
	address = (SERVER_IP_ADDRESS, SERVER_PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(address)
	print "Socket init succeed, waiting for recv packet..."

	while True:
		err = 0
		data, addr = sock.recvfrom(4096)

		if not data:
			print "Has not recvived data."
			continue
		print "Received(", len(data), "):", data, "from", addr

		if (err = parse_packet(data)):
			if DEBUG_LEVEL & DEBUG_LEVEL_ERROR:
				print "Parse packet error:", err
			continue
	sock.close()


if __name__ == "__main__":
	main()	
