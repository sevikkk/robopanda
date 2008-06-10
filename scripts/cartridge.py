#!/usr/local/bin/python

import sys

class EmulationError(Exception):
    pass

class Cartridge:
    def __init__(self, contents, logfile = None):
        self.data = open(contents,'rb').read()
        self.last_addr = None;
        self.log = []
        self.origlog = []
        self.origlog_pos = 0

        if not logfile:
            return 

        linenum = 1
        for line in open(logfile,'r').readlines():
            if line[0] == "#":
                continue

            try:
                line = line.split()
                ts = float(line[0])
                addr = int(line[1],16)
                len = int(line[3][:-1])
            except:
                print linenum, line
                raise

            if ts > 100000:
                break

            linenum += 1
            for a in range(len):
                self.origlog.append((ts, addr+a))

    def orig_lookup(self):
        origlog = self.origlog[self.origlog_pos]
        return origlog[1]

    def spi_emu(self, addr, byte):
        origlog = self.origlog[self.origlog_pos]
        if addr != origlog[1]:
            raise EmulationError,"incorrect read at %.3f, orig addr: %X, emulated addr: %X" % (origlog[0], origlog[1],addr)

        self.origlog_pos += 1

        if (addr - 1) != self.last_addr:
            if self.log:
                print "%9.3f %06X [SPI] %3d: %s" % (self.log[0], self.log[1], len(self.log)-2,
                        " ".join(["%02X" % l for l in self.log[2:]]))
                self.log = []
            self.log.append(origlog[0])
            self.log.append(addr)

        self.last_addr = addr
        self.log.append(byte)

    def read(self, addr, len):
        ret = []
        for a in range(len):
            byte = ord(self.data[addr])
            ret.append(byte)
            if self.origlog:
                self.spi_emu(addr, byte)
            addr += 1
        return ret

    def read_int16(self, addr):
        a,b = self.read(addr,2)
        return a + (b << 8)

    def read_int32(self, addr):
        a,b,c,d = self.read(addr,4)
        return a + (b << 8) + (c << 16) + (d << 24)
