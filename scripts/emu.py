#!/usr/local/bin/python

import sys
from cpu import CPU

class EmulationError(Exception):
    pass

class Cartridge:
    def __init__(self, contents, logfile):
        self.data = open(contents,'rb').read()
        self.last_addr = None;
        self.log = []
        self.origlog = []
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

            #if linenum>100:
            #    break

        self.origlog_pos = 0

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
            self.spi_emu(addr, byte)
            addr += 1
        return ret

    def read_int16(self, addr):
        a,b = self.read(addr,2)
        return a + 256*b

class Player:
    def __init__(self, cartridge):
        self.c = cartridge
        self.state = "idle"
        self.pc = None
        self.codec = None
        self.len = None
        self.start_chunk = 0
        self.data_chunk = 0

    def start(self, ts, addr):
        if self.state != "idle":
            print "%9.3f %06X [PLAY] WARNING: player start in non-idle state: bytes left: %d" % (ts, addr, self.len)
        self.state = "init"
        self.pc = addr

    def nextaddr(self):
        if self.state == "idle":
            return []
        else:
            return [self.pc]

    def do_one_cmd(self, ts, addr):
        if addr != self.pc:
            raise EmulationError, "Player.do_one_cmd with incorrect addr: expected %06X, real %06X" % (self.pc, addr)

        if self.state == "init":
            print "%9.3f %06X [PLAY] init" % (ts, addr)
            data = self.c.read(self.pc,254)
            self.len = data[0] + (data[1]<<8) + (data[2]<<16) + (data[3] <<24)
            self.codec = data[4]
            print "%9.3f %06X [PLAY] INFO: playing audio chunk: %06X %06X %02X" % (ts, addr, self.pc, self.len, self.codec)
            self.pc += 254
            self.len -= 254
            self.state = "init1"
            if self.codec == 7:
                self.start_chunk = 140
                self.data_chunk = 32
            elif self.codec == 9:
                self.start_chunk = 156
                self.data_chunk = 48
        elif self.state == "init1":
            print "%9.3f %06X [PLAY] init1" % (ts, addr)
            self.c.read(self.pc,self.start_chunk)
            self.pc += self.start_chunk
            self.len -= self.start_chunk
            self.state = "data"
        elif self.state == "data":
            print "%9.3f %06X [PLAY] data" % (ts, addr)
            self.c.read(self.pc,self.data_chunk)
            self.pc += self.data_chunk
            self.len -= self.data_chunk
            if self.len == -356: #XXX
                self.state = "idle"
                print "%9.3f %06X [PLAY] INFO: done playing" % (ts, addr)

class Mover:
    def __init__(self, cartridge, index_base, cx_offset):
        self.c = cartridge
        self.state = "idle"
        self.pc = None
        self.ib = index_base
        self.cx_off = cx_offset
        self.stack = []

    def start(self, ts, addr):
        if self.state != "idle":
            print "                 [MOVE] WARNING: mover start in non-idle state"
            return
        print "%9.3f %06X [MOVE] INFO: starting chunk: %04X" % (ts, addr*2 + self.ib, addr)
        self.state = "active"
        self.pc = addr

    def nextaddr(self):
        if self.state == "idle":
            return []
        elif self.state == "active":
            return [self.pc*2 + self.ib]
        elif self.state == "wait":
            return [self.pc*2 + self.ib - 2, self.pc*2 + self.ib]

    def fetch(self, pc):
        return self.c.read_int16(pc * 2 + self.ib)

    def do_one_cmd(self, ts, addr):
        if self.state in ("active", "wait"):
            if self.state == "wait" and addr == self.pc * 2 + self.ib - 2:
                self.pc -= 1

            log_pc = self.pc
            cmd = self.fetch(self.pc)
            self.pc += 1

            if cmd == 0xF000:
                if self.stack:
                    print "%9.3f %06X: [MOVE] [WARNING] Stack not empty" % (ts, addr, log_pc)
                cmd_txt = "done"
                self.state = "idle"
                print "%9.3f %06X [MOVE] INFO: done moving" % (ts, addr)
            elif cmd == 0xF002:
                cmd_txt = "wait_completion"
            elif cmd == 0xF003:
                arg = self.fetch(self.pc)
                self.pc += 1
                cmd_txt = "wait_completion_max %d" % (arg,)
            elif cmd in (0xF004,0xF00D):
                self.state = "wait"
                cmd_txt = "wait_%02X" % (cmd & 0xFF)
            elif cmd == 0xF005:
                arg = self.fetch(self.pc)
                self.pc += 1
                cmd_txt = "delay %d" % (arg,)
            elif cmd == 0xF006:
                arg = self.fetch(self.pc)
                self.stack.append(self.pc + 1)
                self.pc = arg
                cmd_txt = "call %06X // stack: %s" % (arg,self.dump_stack())
            elif cmd == 0xF00A:
                if self.stack:
                    self.pc = self.stack.pop()
                else:
                    self.state = "idle"
                    print "%9.3f %06X [MOVE] INFO: done moving" % (ts, addr)
                cmd_txt = "return"
            else:
                cmd_txt = "cmd_%04X" % (cmd)
                self.state = "active"

            print "%9.3f %06X [MOVE] %06X: %s" % (ts, addr, log_pc, cmd_txt)


def main():
    c = Cartridge(sys.argv[1], sys.argv[2])
    magic = c.read_int16(0)
    print "                 [INFO] Magic: %04X" % magic
    index_base = c.read_int16(2)
    print "                 [INFO] IndexBase: %04X" % index_base
    version_ptr = c.read_int16(index_base + 2)
    print "                 [INFO] VersionPtr: %04X (%06X)" % (
                                        version_ptr, 
                                        version_ptr*2 + index_base)
    version = c.read_int16(version_ptr*2 + index_base)
    print "                 [INFO] Version: %04X" % version
    mover_scripts_ptr = c.read_int16(index_base + 4)
    print "                 [INFO] MoverScriptsPtr: %04X (%06X)" % (
                                        mover_scripts_ptr,
                                        mover_scripts_ptr*2+index_base)
    cmdCX_offset = c.read_int16(index_base + 6)
    print "                 [INFO] cmdCX_offset: %04X" % cmdCX_offset
    start = c.read_int16(index_base + 8)
    print "                 [INFO] start pc: %04X (%06X)" % (
                                        start, 
                                        start*2+index_base)
    smth = c.read_int16(index_base + 0xA)
    print "                 [INFO] Something: %04X" % (smth)
    mover_scripts_num = c.read_int16(mover_scripts_ptr*2 + index_base - 2)
    print "                 [INFO] MoverScriptsNum: %d" % (mover_scripts_num,)

    mover = Mover(c, index_base, cmdCX_offset)
    player = Player(c)
    cpu = CPU(c, index_base, cmdCX_offset, start, mover, player)

    while 1:
        if c.origlog_pos > (len(c.origlog) - 5):
            break

        ts, next_addr = c.origlog[c.origlog_pos]

        next_addrs = mover.nextaddr()
        if next_addr in next_addrs:
            mover.do_one_cmd(ts, next_addr)
            continue

        next_addrs = player.nextaddr()
        if next_addr in next_addrs:
            player.do_one_cmd(ts, next_addr)
            continue

        cpu.do_one_cmd(ts, next_addr)

if __name__ == "__main__":
    main()
