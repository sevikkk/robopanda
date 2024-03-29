#!/usr/local/bin/python

import struct

key32 = "00 00 00 00 00 00 00 00 18 11 11 11 18 11 11 11 18 11 11 11 18 11 55 18 11 55 58 88 88 88 88 88".split()
key32 = [int(a,16) for a in key32]
key48 = "00 00 00 00 00 00 00 00 18 11 11 11 18 11 11 11 18 11 11 11 18 11 11 11 18 11 11 11 18 11 11 11 18 11 55 18 11 55 58 55 58 55 58 58 58 58 58 58".split()
key48 = [int(a,16) for a in key48]


def main(fn):
    out_hdr = ""
    out_data = []
    hist = {}
    for i in range(32*8):
        hist[i] = [0,0]

    for f in fn:
        data = open(f,'rb').read()
        print f,ord(data[0]), ord(data[1])
        out_hdr = data[:2]
        out_foot = data[-4:]

        data = data[2:-4]
        while 1:
            d = data[:32]
            data = data[32:]

            if not d:
                break

            txt = []
            ndata = []
            for i in range(32):
                ndata.append(ord(d[i]) ^ key[i])
                txt.append("%02X" % ndata[i])
                out_data.append(ndata[i])

            print " ".join(txt)

            for i in range(32):
                cc = ndata[i]
                for ii in range(8):
                    if cc &0x80:
                        hist[i*8 + ii][1] += 1
                    else:
                        hist[i*8 + ii][0] += 1

                    cc = cc<<1;
        of = open("out.aud","wb")
        of.write(out_hdr)

        out_data = out_data[1:]
        out_data.append(0)
        while out_data:
            ndata = []
            for i in range(32):
                ndata.append(chr(out_data[i] ^ key[i]))
            of.write("".join(ndata))
            out_data = out_data[32:]
        of.write(out_foot)
        of.close()

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

