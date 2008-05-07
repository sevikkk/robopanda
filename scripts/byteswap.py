#!/usr/local/bin/python
import sys
import struct

f = open("cartridge.bin","r")
f2=open("cartridge_swap.bin","w")
while 1:
    d = f.read(4)
    if d == "":
        break
    z = struct.unpack(">L",d)
    d = struct.pack("<L",z[0])
    f2.write(d)

