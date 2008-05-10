#!/usr/local/bin/python

import struct
import os

def main(fn):
    data = open(fn,'r').read()
    try:
        os.mkdir("dump")
    except:
        pass

    print "============== Audio data ======================"
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
    mover_scripts_end = struct.unpack('<H',data[index_base+2:index_base+4])[0]
    mover_scripts = struct.unpack('<H',data[index_base+4:index_base+6])[0]
    mover_scripts = mover_scripts * 2 + index_base
    mover_scripts_num = struct.unpack('<H',data[mover_scripts-2:mover_scripts])[0]
    cx_offset = struct.unpack('<H',data[index_base+6:index_base+8])[0]
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
    if 0:
        for addr in addrs_keys:
            if addr in aliases:
                aliases_str = " aliases: " +",".join([ "%d" % a for a in aliases[addr]])
            else:
                aliases_str = ""

            print "Script%05d: %04X (%06X)%s" % (addrs[addr], addr, index_base + addr*2, aliases_str)

    print "============== Mover Scripts ======================"
    addr = addrs_keys[0]
    while addr<mover_scripts_end:
        if addr in addrs:
            print "scr%d:" % addrs[addr]
            if addr in aliases:
                for a in aliases[addr]:
                    print "scr%d:" % a

        spi_addr = addr*2+index_base
        cmd = struct.unpack('<H',data[spi_addr:spi_addr+2])[0]
        if (cmd & 0xF000) == 0xF000:
            if cmd == 0xF000:
                cmd_txt = "done"
            elif cmd == 0xF001:
                cmd_txt = "ctrl_F001"
            elif cmd == 0xF002:
                cmd_txt = "wait_completion"
            elif cmd == 0xF003:
                arg = struct.unpack('<H',data[spi_addr+2:spi_addr+4])[0]
                cmd_txt = "wait_completion_max %d" % arg
                addr += 1
            elif cmd == 0xF004:
                cmd_txt = "wait_04"
            elif cmd == 0xF005:
                arg = struct.unpack('<H',data[spi_addr+2:spi_addr+4])[0]
                cmd_txt = "wait_completion_max %d" % arg
                addr += 1
            elif cmd == 0xF006:
                arg = struct.unpack('<H',data[spi_addr+2:spi_addr+4])[0]
                if arg in addrs:
                    label = "scr%d" % addrs[arg]
                else:
                    label = "%04X" % arg

                cmd_txt = "call %s" % label
                addr += 1
            elif cmd == 0xF007:
                cmd_txt = "ctrl_F007"
            elif cmd == 0xF008:
                cmd_txt = "ctrl_F008"
            elif cmd == 0xF009:
                cmd_txt = "ctrl_F009"
            elif cmd == 0xF00A:
                cmd_txt = "return"
            elif cmd == 0xF00B:
                cmd_txt = "ctrl_F00B"
            elif cmd == 0xF00C:
                cmd_txt = "ctrl_F00C"
            elif cmd == 0xF00D:
                cmd_txt = "wait_0D"
            elif cmd == 0xF00E:
                cmd_txt = "ctrl_F00E"
            elif cmd == 0xF00F:
                cmd_txt = "ctrl_F00F"
            else:
                cmd_txt = "ctrl_%04X" % cmd
        else:
                cmd_txt = "cmd_%04X" % cmd

        print "\t%04X: %s" % (addr, cmd_txt)
        addr += 1

    print "=================== Code ======================="
    addr = 0x3C
    while addr < 0x6473:

        spi_addr = addr*2+index_base

        cmd = struct.unpack('<H',data[spi_addr:spi_addr+2])[0]
        arg2 = struct.unpack('<H',data[spi_addr+2:spi_addr+4])[0]
        arg3 = struct.unpack('<H',data[spi_addr+4:spi_addr+6])[0]

        next_addr = addr + 1
        cmd_txt = ""

        if cmd & 0xFE00 == 0:
            arg = cmd & 0x1FF
            if arg == 0x1FF:
                cmd_name = "push2"
                arg = arg2
                next_addr += 1
            else:
                cmd_name = "push"

            cmd_txt = "%s %04X" % (cmd_name, arg)
        elif cmd == 0x2978:
            cmd_txt = "return"
        elif cmd == 0x2979:
            cmd_txt = "return_f0"
        elif cmd == 0x2928:
            cmd_txt = "play"
        elif cmd == 0x292f:
            cmd_txt = "move"
        elif cmd & 0xF000 == 0xB000:
            arg = cmd & 0xfff
            if arg == 0xFFF:
                arg = arg2
                cmd_name = "spi_read2"
                next_addr += 1
            else:
                cmd_name = "spi_read"
            cmd_txt = "%s %04X" % (cmd_name, arg)
        elif cmd & 0xE000 == 0xC000:
            arg = cmd & 0x1FFF
            if arg == 0x1FFF:
                cmd_name = "call2"
                arg = arg2
                next_addr += 1
                flags = struct.unpack('BB',data[spi_addr+4:spi_addr+6])
            else:
                cmd_name = "call"
                flags = struct.unpack('BB',data[spi_addr+2:spi_addr+4])

            next_addr += 1
            cmd_txt = "%s %04X(%d,%d)" % (cmd_name, arg + cx_offset, flags[1], flags[0])
        elif cmd & 0xE000 == 0xE000:
            subcmd = (cmd & 0x1800)>>11
            offset = (cmd & 0x7FF)

            if offset & 0x400 != 0:
                offset = offset - 0x801

            arg2_txt = ""

            if subcmd == 0:
                cmd_name = "rjump"
            elif subcmd == 1:
                cmd_name = "rjump_e8"
            elif subcmd == 2:
                cmd_name = "rjump_f0"
            elif subcmd == 3:
                cmd_name = "rjump_arg"
                arg2_txt = ",%04X" % arg2
                next_addr += 1

            arg = addr + offset + 1

            cmd_txt = "%s %04X%s" % (cmd_name, arg, arg2_txt)

        hex = "%04X" % cmd

        if next_addr > addr + 1:
            hex += " %04X" % arg2
        else:
            hex += "     "

        if next_addr > addr + 2:
            hex += " %04X" % arg3
        else:
            hex += "     "

        if not cmd_txt:
            cmd_txt = "unknown %04X" % cmd

        print "%04X: %s %s" % (addr, hex, cmd_txt)

        addr = next_addr

if __name__ == "__main__":
    import sys
    main(sys.argv[1])

