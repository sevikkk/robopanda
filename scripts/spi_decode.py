#!/usr/local/bin/python

import sys
import struct

class DecodeError(Exception):
    pass

def main():
    fn = sys.argv[1]
    f = open(fn,"rb")
    d = f.read(5120)

    pts = 0
    pcnt = 0
    ts_rolls = 0
    cnt_rolls = 0

    while 1:
        d = f.read(8)
        if d == "":
            break

        d1,d2 = struct.unpack("<LL",d)
        if d1 == 0xCEBA1234:
            break

        """
        1 word:
            31:29 - 3
            28:25 - cmd_id
            24:16 - byte_cnt
            15:0 - ts[20:5]

        2 word:
            31:29 - 5
            28:25 - cmd_id
            24 - 1
            23:0 - addr
        """
        cmd = (d1 >> 29) & 0x7
        cnt = (d1 >> 25) & 0xf
        byte_cnt = (d1>>16) & 0x1ff
        ts = d1 & 0xffff

        cmd2 = (d2 >> 29) & 0x7
        cnt2 = (d2 >> 25) & 0xf
        addr = d2 & 0xffffff

        if cmd == 3 and cmd2 == 1:
            print "# incorrect command: cmd: %d, cmd2: %d, cnt: %d, cnt2: %d, data: %04X %04X" % (cmd, cmd2, cnt, cnt2, d1, d2)
            continue

        if cmd != 3 or cmd2 != 5 or cnt != cnt2:
            print cmd, cmd2
            raise DecodeError, "at %X" % f.tell()

        dts = ts - pts

        if dts<-32768:
            ts_rolls += 1
            dts += 65536

        dcnt = cnt - pcnt
        if dcnt<-8:
            cnt_rolls += 1
            dcnt += 16

        #print "%8.3f %06X %06X %2d: %s # %d %d %d %d" % ((ts +65536 * ts_rolls)*12.5*32/1000/1000, addr, addr/2, byte_cnt, "??", ts + 65536 * ts_rolls, dts, 16 * cnt_rolls + cnt, dcnt)
        print "%10.3f %06X %06X %2d: ?? # %d" % ((ts +65536 * ts_rolls)*12.5*32/1000/1000, addr, addr/2, byte_cnt, dcnt)

        pts = ts
        pcnt = cnt


if __name__ == "__main__":
    main()
