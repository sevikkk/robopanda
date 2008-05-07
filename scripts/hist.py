#!/usr/local/bin/python

import struct

def main(fn):
    hist = {}
    for i in range(32*8):
        hist[i] = [0,0]
    for f in fn:
        data = open(f,'r').read()
        print f,ord(data[0]), ord(data[1])
        data = data[2:-4]
        continue
        while 1:
            d = data[:32]
            data = data[32:]
            if not d:
                break
            for i in range(32):
                cc = ord(d[i])
                for ii in range(8):
                    if cc &0x80:
                        hist[i*8 + ii][1] += 1
                    else:
                        hist[i*8 + ii][0] += 1

                    cc = cc<<1;
    return

    for i in range(32*8):
         s = 100.0/(hist[i][0]+hist[i][1])
         v0 = s*hist[i][0]
         v1 = s*hist[i][1]
         sv = abs(v0 - 50)+50
         if v0>v1:
             c = "0"
         else:
             c = "1"
         if sv<60:
             st = ""
         elif sv<70:
             st = c
         elif sv<90:
             st = c*2
         else:
             st = c*3

         print "%5d %5s %5d %5d" % (i, st, s*hist[i][0],s*hist[i][1])


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

