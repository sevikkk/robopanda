#!/usr/local/bin/python
import sys

class InputError(Exception):
    pass

def main(input, cartridge):

    data = open(cartridge,"rb").read()
    for a in open(input, "r").readlines():
        if a[0] == "#":
            continue
        a = a.split()
        if len(a) < 4:
            raise InputError, "invalid input string: %s" % (`a`)
        ts, addr1, addr2, nb = a[:4]
        ts = float(ts)
        addr = int(addr1, 16)
        nb = int(nb[:-1])
        bytes = []
        for a in range(nb):
            bytes.append("%02X" % ord(data[addr+a]))

        print "%9.3f %s %s %d: %s" % (ts, addr1, addr2, nb, " ".join(bytes))

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

