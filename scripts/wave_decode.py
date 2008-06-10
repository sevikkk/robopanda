#!/usr/local/bin/python

import sys
import struct

class Logger:
    def __init__(self):
        self.state = "start"
        self.cmd = 0
        self.ts = 0
        self.addr = 0
        self.bytes = []

    def restart(self, ts):
        if self.cmd:
            print "%8.3f %06X %06X %2d: %s" % (self.ts*12.5/1000/1000, self.addr, self.addr/2, len(self.bytes), " ".join(self.bytes))

        self.cmd = "none"
        self.ts = ts
        self.addr = 0
        self.bytes = []

        self.state = "cmd"

    def input(self, ts, ib, ob):
        if self.state == "cmd":
            if ib == 3:
                self.cmd = "read"
                self.state = "addr0"
            else:
                self.cmd = "unk%d" % ib
                self.state = "unknown"
        elif self.state == "unknown":
            self.bytes.append("(%02X,%02X)" % (ib, ob))
        elif self.state == "addr0":
            self.state = "addr1"
            self.addr += ib*256*256
        elif self.state == "addr1":
            self.state = "addr2"
            self.addr += ib*256
        elif self.state == "addr2":
            self.state = "data"
            self.addr += ib
        elif self.state == "data":
            self.bytes.append("%02X" % (ob,))


def main():
    fn = sys.argv[1]
    f = open(fn,"rb")
    d = f.read(5120)

    log = Logger()

    with_verilog = 0
    with_wave = 0

    if with_verilog:
        ver_test = open("tb.v","w")

    pts = 0
    pcnt = 0
    ts_rolls = 0
    cnt_rolls = 0
    pclk = 0
    bitcnt = 0

    si_byte = 0
    so_byte = 0

    while 1:
        d = f.read(4)
        if d == "":
            break

        d1,d2,d3,d4 = struct.unpack("BBBB",d)
        if (d1,d2,d3,d4) ==  (0x34,0x12,0xBA,0xCE):
            break

        ts = d1 + d2*256
        cnt = d3 + (d4 & 0xf) * 256
        cs = d4 & 0x80 and "cs" or "--"
        clk = d4 & 0x40 and "clk" or "---"
        si = d4 & 0x20  and "si" or "--"
        so = d4 & 0x10  and "so" or "--"
        dts = ts - pts

        if dts<-30000:
            ts_rolls += 1
            dts += 65536

        dcnt = cnt - pcnt
        if dcnt<-2000:
            cnt_rolls += 1
            dcnt += 4096

        if cs == "cs":
            bitcnt = -1
            log.restart(ts + 65536 * ts_rolls)

        si_prn = ""
        so_prn = ""

        if clk != pclk and clk == "clk":
            bitcnt += 1

            si_byte = si_byte << 1
            so_byte = so_byte << 1
            if si == "si":
                si_byte += 1
            if so == "so":
                so_byte += 1

            if bitcnt % 8 == 7:
                log.input(ts + 65536 * ts_rolls, si_byte,so_byte)
                si_prn = "%02X" % si_byte
                so_prn = "%02X" % so_byte
                si_byte = 0
                so_byte = 0

        pclk = clk

        #print "%7x %7d %7d %5d %5d %s %s %s %s" % (ts, ts_rolls*65536 + ts, dts, cnt_rolls*4096 + cnt,dcnt,cs,clk,si,so)
        if with_wave:
            print "%10d %5d %s %s %s %s %d %s %s" % (ts_rolls*65536 + ts, dts, cs, clk, si, so, bitcnt, si_prn, so_prn)

        if with_verilog:
            ver_test.write("""
                #%d; // time: %d ns
                spi_cs = %d;
                spi_clk = %d;
                spi_si = %d;
                spi_so = %d;
            """ % (dts*12, (ts_rolls*65536 + ts) * 12,
                    (cs == "cs") and 1 or 0,
                    (clk == "clk") and 1 or 0,
                    (si == "si") and 1 or 0,
                    (so == "so") and 1 or 0,
                ))

        pts = ts
        pcnt = cnt

    if with_verilog:
        ver_test.close()

if __name__ == "__main__":
    main()
