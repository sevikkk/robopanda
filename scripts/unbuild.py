#!/usr/local/bin/python

import struct
import os

def main(fn):
    data = open(fn,'r').read()
    try:
        os.mkdir("dump")
    except:
        pass
    addr = 5
    n = 0
    while 1:
        a = data[addr:addr+4]
        a = struct.unpack('<L',a)[0]
        a = a & 0xffffff

        l = data[a:a+4]
        l = struct.unpack('<L',l)[0]
        if l == 0:
            break
        format = data[a+4:a+6]
        format = struct.unpack("BB",format)

        print "Audio%05d: %06X %d %s" % (n, a, l, format)
        f = open("dump/%05d.aud" % n,"w")
        f.write(data[a+4:a+l+4])
        f.close()
        addr += 3
        n += 1

    index_base = struct.unpack('<H',data[2:4])[0]
    mover_scripts = struct.unpack('<H',data[index_base+4:index_base+6])[0]
    mover_scripts = mover_scripts * 2 + index_base
    mover_scripts_num = struct.unpack('<H',data[mover_scripts-2:mover_scripts])[0]
    addrs = {}
    aliases = {}
    for i in range(mover_scripts_num):
        addr = struct.unpack('<H',data[mover_scripts+i*2:mover_scripts+i*2+2])[0]
        if addr in addrs:
            if not addr in aliases:
                aliases[addr] = []
            aliases[addr].append(i)
        else:
            addrs[addr] = i

    addrs_keys = addrs.keys()
    addrs_keys.sort()
    for addr in addrs_keys:
        if addr in aliases:
            aliases_str = " aliases: " +",".join([ "%d" % a for a in aliases[addr]])
        else:
            aliases_str = ""

        print "Script%05d: %06X%s" % (addrs[addr],addr,aliases_str)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])

