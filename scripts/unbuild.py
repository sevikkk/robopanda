#!/usr/local/bin/python

import struct
import os
import bisect
from cpu import CPU
from cartridge import Cartridge

def main(fn):
    cartridge = Cartridge(fn)

    try:
        os.mkdir("dump")
    except:
        pass

    print "============== Audio data ======================"
    addr = 5
    n = 1
    while 1:
        a = cartridge.read_int32(addr)
        a = a & 0xffffff

        l = cartridge.read_int32(a)
        if l == 0:
            break

        format = cartridge.read_int16(a+4)

        print "Audio%05d: %06X %d %s" % (n, a, l, format)
        f = open("dump/%05d.aud" % n,"wb")
        f.write(cartridge.data[a+4:a+l+4])
        f.close()
        addr += 3
        n += 1

    index_base = cartridge.read_int16(2)
    mover_scripts_end = cartridge.read_int16(index_base+2)
    mover_scripts = cartridge.read_int16(index_base+4)
    mover_scripts_spi = mover_scripts * 2 + index_base
    mover_scripts_num = cartridge.read_int16(mover_scripts_spi - 2)
    cx_offset = cartridge.read_int16(index_base+6)
    addrs = {}
    aliases = {}
    for i in range(mover_scripts_num):
        addr = cartridge.read_int16(mover_scripts_spi + i*2)
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
        cmd = cartridge.read_int16(spi_addr)
        if (cmd & 0xF000) == 0xF000:
            if cmd == 0xF000:
                cmd_txt = "done"
            elif cmd == 0xF001:
                cmd_txt = "ctrl_F001"
            elif cmd == 0xF002:
                cmd_txt = "wait_completion"
            elif cmd == 0xF003:
                arg = cartridge.read_int16(spi_addr+2)
                cmd_txt = "wait_completion_max %d" % arg
                addr += 1
            elif cmd == 0xF004:
                cmd_txt = "wait_04"
            elif cmd == 0xF005:
                arg = cartridge.read_int16(spi_addr+2)
                cmd_txt = "wait_completion_max %d" % arg
                addr += 1
            elif cmd == 0xF006:
                arg = cartridge.read_int16(spi_addr+2)
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

    xrefs_code_local = {}
    xrefs_code_global = {}
    xrefs_data = {}
    xrefs_globals = {}
    barriers = {}
    labels = {}

    def add_xref(addr, typ, ref):
        #print "add xref %s %04X -> %04X" % (typ, addr, ref)
        if typ == "code_local":
            xrefs = xrefs_code_local
        elif typ == "code_global":
            xrefs = xrefs_code_global
        elif typ == "data":
            xrefs = xrefs_data
        elif typ == "globals":
            xrefs = xrefs_globals
        else:
            return

        if not ref in xrefs:
            xrefs[ref] = {}

        xrefs[ref][addr] = 1

    barriers_list = []

    print "=================== Code ======================="
    for pass_num in (1,2):
        addr = 0x20
        cpu = CPU(cartridge, index_base, cx_offset, addr, None, None)
        cpu.labels = labels
        barriers[addr] = 1
        while addr < mover_scripts-1:
            spi_addr = addr * 2 + index_base
            decoded = cpu.decode(addr)
            if decoded.barrier:
                barriers[addr+1] = 1
            for typ, ref in decoded.xrefs:
                add_xref(addr,typ, ref)

            hex = []
            for i in range(decoded.cmd_len):
                hex.append("%04X" % cartridge.read_int16(spi_addr + i * 2))
            hex = " ".join(hex)

            if pass_num == 2:
                if addr in barriers_list:
                    print "//------------------------------------------------------------------"
                if addr in xrefs_code_global:
                    print "// global entry, xrefs: ",",".join(["%04X"%d for d in xrefs_code_global[addr]])
                if addr in xrefs_data:
                    print "// data entry, xrefs: ",",".join(["%04X"%d for d in xrefs_data[addr]])
                if addr in labels:
                    print "     %20s:                                // xrefs: %s" % (labels[addr],",".join(["%04X"%d for d in xrefs_code_local[addr]]))
                print "%04X: %-20s %-9s %-20s // %s" % (addr, hex, 
                        decoded.cmd, decoded.args or "", decoded.descr or "")

            addr += decoded.cmd_len

        barriers[addr] = 1

        if pass_num == 1:
            barriers_list = barriers.keys()
            barriers_list.sort()
            #print "barriers", barriers_list[:10]
            for ref in xrefs_code_local:
                ref_idx = bisect.bisect(barriers_list,ref) - 1
                #print "barrs", ref_idx, ref, barriers_list[ref_idx]
                for addr in xrefs_code_local[ref]:
                    addr_idx = bisect.bisect(barriers_list,addr) - 1
                    if ref_idx != addr_idx:
                        #print "cross area jump: %04X %04X %d %d" % (addr, ref, addr_idx, ref_idx)
                        if ref_idx<addr_idx:
                            start_idx = ref_idx
                            end_idx = addr_idx
                        else:
                            start_idx = addr_idx
                            end_idx = ref_idx
                        if end_idx - start_idx<10:
                            for idx in range(start_idx,end_idx):
                                try:
                                    #print "delete barrier", barriers_list[start_idx+1]
                                    del barriers_list[start_idx+1]
                                except IndexError:
                                    pass
                        else:
                            print "%04X: too long cross area jump %d -> %d, ignoring" % (addr, addr_idx, ref_idx)
                    else:
                        #print "intra area jump: %04X %04X %d %d" % (addr, ref, addr_idx, ref_idx)
                        pass

            labels = {}
            refs = xrefs_code_local.keys()
            refs.sort()
            last_area = -1
            label_cnt = 0
            for ref in refs:
                ref_idx = bisect.bisect(barriers_list,ref) - 1
                if ref_idx != last_area:
                    label_cnt = 1
                    last_area = ref_idx
                labels[ref] = "L%d_%d" % (ref_idx, label_cnt)
                label_cnt += 1
    print "=================== Globals ======================="
    refs = xrefs_globals.keys()
    refs.sort()
    for ref in refs:
        print "%04X %s" % (ref,",".join(["%04X"%d for d in xrefs_globals[ref].keys()]))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])

