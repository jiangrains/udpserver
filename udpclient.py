# --*-- coding:utf-8 -*-
import socket
import struct

address = ('192.168.1.12', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

length = 24
INSOLE_VERSION = 0x1
PACKET_TYPE_REGISTER_RESPONSE = 0x1
sn = "#000000000000001"
PACKET_MAGICNUM = 0xffffffff
register_packet = struct.pack("!H2b16sI", length, INSOLE_VERSION, PACKET_TYPE_REGISTER_RESPONSE, sn, PACKET_MAGICNUM)
s.sendto(register_packet, address)

s.close()  
