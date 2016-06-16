# --*-- coding:utf-8 -*-
import socket
import struct

address = ('192.168.1.12', 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

length = 28 + 24*2
INSOLE_VERSION = 0x1
PACKET_TYPE_LOCATION = 0x3
sn = "#000000000000002"
PACKET_MAGICNUM = 0xffffffff
status = 0x1
reserve = 0x0
cellnum = 2
header = struct.pack("!H2b16sI2bH", length, INSOLE_VERSION, PACKET_TYPE_LOCATION, sn, PACKET_MAGICNUM, status, reserve, cellnum)

mcc = 0x460
mnc = 0x0
lac = 0x247f
cid = 0x0f67
bsic = 0x11
rxl = 0x22
data1 = struct.pack("!6I", mcc, mnc, lac, cid, bsic, rxl)

mcc = 0x460
mnc = 0x0
lac = 0x247f
cid = 0x0ebd
bsic = 0x71
rxl = 0x55
data2 = struct.pack("!6I", mcc, mnc, lac, cid, bsic, rxl)


packet = struct.pack("!28s24s24s", header, data1, data2)

s.sendto(packet, address)

s.close()  
