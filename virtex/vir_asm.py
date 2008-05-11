#!/usr/local/bin/python

import struct

class Ram:
    def __init__(self):
        self.data = {}
        self.pc = 0

        self.labels = {}
        self.backrefs = {}

    def append(self, cmd):
        if type(cmd) == type([]):
            for a in cmd:
                self.append(a)
            return
        self.data[self.pc] = cmd
        self.pc += 1

    def img(self):
        addrs = self.data.keys()
        addrs.sort()
        max = addrs[-1]
        img = []
        for i in range(max+1):
            img.append(self.data.get(i,0))

        return img

    def dump(self):
        img = self.img()
        bin = []
        txt = []
        addr = 0
        for a in img:
            bin.append(struct.pack(">L",a))
            txt.append("\t\t\t\t\t%d: int_ram_data <= 32'h%08x;\r\n" % (addr, a))
            addr += 1
        txt.append("\t\t\t\t\t%d: begin\r\n" % (addr))
        open("prg.bin","w").write("".join(bin))
        open("prg.txt","w").write("".join(txt))

    read_write_args = {
            "uart":     (0, "rw"),
            "idx":      (1, "rw"),
            "idx2":     (2, "rw"),
            "cnt":      (3, "rw"),
            "r0":       (4, "rw"),
            "r1":       (5, "rw"),
            "r2":       (6, "rw"),
            "r3":       (7, "rw"),
            "@idx":     (8, "r"),
            "@idx+":    (9, "r"),
            "@idx2":    (8, "w"),
            "@idx2+":   (9, "w"),
    }

    def get_int(self, s):
        if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
            return ord(s[1])
        return int(s,0)

    def cmd(self, s):
        s = s.split('//',1)
        s = s[0]

        s = s.split(None,1)
        if len(s) == 0:
            return []
        elif len(s) == 1:
            cmd = s[0]
            arg = ""
            args = []
        else: # 2
            cmd, arg = s
            args = arg.strip()
            args = args.split()
            args = "".join(args).split(",")

        cmd = cmd.lower()

        if cmd[-1] == ":" and len(args) == 0:
            label = cmd[:-1]
            if label in self.labels:
                raise SyntaxError, s

            self.labels[label] = self.pc
            if label in self.backrefs:
                for a in self.backrefs[label]:
                    self.data[a] = self.data.get(a,0) + self.pc

            return []

        if cmd == ".org" and len(args) == 1:
            self.pc = int(args[0],0)
            return []

        if cmd == "writeuart":
            if (arg[0] == '"' and arg[-1] == '"') or (arg[0] == "'" and arg[-1] == "'"):
                args = eval(arg)
                return self.writeuart_str(args)

            if len(args) == 2 and args[0] == "acc" and args[1] in ('hex1','hex2','hex3','hex4'):
                l = 4 - int(args[1][3])
                return (1<<28) + (1<<26) + (l<<24)

            raise SyntaxError, s

        if cmd == "jump" or cmd == "loop":
            addr = 0
            addr_ok = 0
            if len(args) > 0 and args[0][0] == "#":
                addr = int(args[0][1:],0)
                addr_ok = 1

            if len(args) > 0 and args[0][0] == "$":
                label = args[0][1:]
                if label in self.labels:
                    addr = self.labels[label]
                else:
                    if not label in self.backrefs:
                        self.backrefs[label] = []

                    self.backrefs[label].append(self.pc)

                    addr = 0
                addr_ok = 1

            code = (2<<28) + addr
            if cmd == "loop" and len(args) == 1 and addr_ok:
                return code + (15<<24)

            if cmd == "loop":
                raise SyntaxError, s

            if len(args) == 1 and addr_ok:
                return code

            if len(args) == 1 and args[0] == "acc":
                return code + (14<<24)

            if len(args) != 2:
                raise SyntaxError, s

            if args[1] == "rx_rdy":
                return code + (1<<24)

            if args[1] == "!rx_rdy":
                return code + (2<<24)

            if args[1] == "tx_empty":
                return code + (3<<24)

            if args[1] == "!tx_empty":
                return code + (4<<24)

            raise SyntaxError, s
        if cmd == "skip":
            if len(args) != 1:
                raise SyntaxError, s

            code = (2<<28) 

            if args[0][0] == "=":
                val = self.get_int(args[0][1:])
                return code + (5<<24) + val

            if args[0][0] == "!":
                val = self.get_int(args[0][1:])
                return code + (6<<24) + val

            raise SyntaxError, s

        if cmd == "read" or cmd == "write":
            if len(args) != 1:
                raise SyntaxError, s

            if cmd == "read":
                code = (3<<28)
            else:
                code = (4<<28)

            if args[0] in self.read_write_args:
                c, m = self.read_write_args[args[0]]
                if cmd == "read" and not "r" in m:
                    raise SyntaxError, s
                if cmd == "write" and not "w" in m:
                    raise SyntaxError, s

                return code + (c<<24)

            if args[0][0] == "@":
                addr = int(args[0][1:],0)
                return code + (10<<24) + addr

            if cmd != "read":
                raise SyntaxError, s

            if args[0][0] == "#":
                val = int(args[0][1:],0)
                if val < 0x1000000:
                    return code + (14<<24) + val
                else:
                    return [
                            code + (14<<24) + (val & 0xffffff),
                            code + (15<<24) + ((val >>24 ) & 0xff)
                        ]
        if cmd in ("readwb", "writewb", "readdram","writedram"):
            if len(args) != 1:
                raise SyntaxError, s
            if args[0] in ('@idx','@idx+','@idx2','@idx2+'):
                code = {
                        ("readdram","@idx"):
                            (1<<28) + (3<<26) + (0<<24),
                        ("readdram","@idx+"):
                            (1<<28) + (3<<26) + (2<<24),
                        ("writedram","@idx2"):
                            (1<<28) + (3<<26) + (1<<24),
                        ("writedram","@idx2+"):
                            (1<<28) + (3<<26) + (3<<24),
                }.get((cmd, args[0]))

                if not code:
                    raise SyntaxError, s

                return code

            if args[0][0] != "@":
                raise SyntaxError, s

            addr = int(args[0][1:],0)
            code = {
                "readwb":
                    (1<<28) + (2<<26) + (0<<24),
                "writewb":
                    (1<<28) + (2<<26) + (1<<24),
                "readdram":
                    (1<<28) + (2<<26) + (2<<24),
                "writedram":
                    (1<<28) + (2<<26) + (3<<24),
                }.get(cmd)

            if not code:
                raise SyntaxError, s

            return code + addr

        if cmd == "shift":
            if len(args) != 1:
                raise SyntaxError, s
            code = {
                "left1":
                    (5<<28) + (0<<24) + (0<<20),
                "left8":
                    (5<<28) + (0<<24) + (1<<20),
                "right1":
                    (5<<28) + (0<<24) + (2<<20),
                "right8":
                    (5<<28) + (0<<24) + (3<<20),
                }.get(args[0])

            if not code:
                raise SyntaxError, s

            return code
        code, m = {
            "andl": ( (5<<28) + (1<<24) + (0<<20), "i" ),
            "andh": ( (5<<28) + (1<<24) + (1<<20), "i" ),
            "orl":  ( (5<<28) + (1<<24) + (2<<20), "i" ),
            "orh":  ( (5<<28) + (1<<24) + (3<<20), "i" ),
            "xorl": ( (5<<28) + (1<<24) + (4<<20), "i" ),
            "xorh": ( (5<<28) + (1<<24) + (5<<20), "i" ),
            "addl": ( (5<<28) + (1<<24) + (6<<20), "i" ),
            "addh": ( (5<<28) + (1<<24) + (7<<20), "i" ),
            "subl": ( (5<<28) + (1<<24) + (8<<20), "i" ),
            "subh": ( (5<<28) + (1<<24) + (9<<20), "i" ),

            "sub":  ( (5<<28) + (1<<24) + (12<<20), "r" ),
            "and":  ( (5<<28) + (2<<24) +  (0<<20), "r" ),
            "or":   ( (5<<28) + (2<<24) +  (4<<20), "r" ),
            "xor":  ( (5<<28) + (2<<24) +  (8<<20), "r" ),
            "add":  ( (5<<28) + (2<<24) + (12<<20), "r" ),
        }.get(cmd, (0,0))

        if code and m == "i":
            if len(args) != 1:
                raise SyntaxError, s

            if args[0][0] != "#":
                raise SyntaxError, s

            val = self.get_int(args[0][1:])

            return code + val

        if code and m == "r" and args[0] in ("r0","r1","r2","r3"):
            if len(args) != 1:
                raise SyntaxError, s
            r = int(args[0][1])

            return code + (r<<20)
            


        raise SyntaxError, s

    def writeuart_str(self, s):
        res = []
        while s:
            ss = s[:3]
            cmd = (1<<28) + (0<<26)
            cmd += ord(ss[0])<<16
            if len(ss)>1:
                cmd += (ord(ss[1])<<8) + (1<<25)
            if len(ss)>2:
                cmd += ord(ss[2]) + (1<<24)

            res.append(cmd)
            s = s[3:]

        return res

def dump_res(res):
    if type(res) == type([]):
        s = []
        for a in res:
            s.append("0x%08x" % (a, ))

        return "[" + ", ".join(s) + "]"
    else:
        return "0x%08x" % (res, )

def test():
    ram = Ram()
    #ram.writeuart_imm("bubu!\r\nok> ")
    #ram.jump(ram.pc)
    #ram.dump()
    res = ram.cmd(" writeuart 'bubu\\r\\n'")
    assert res == [0x13627562, 0x13750d0a]

    res = ram.cmd(" writeuart 'bu bu\\r\\n'")
    assert res == [0x13627520, 0x1362750d, 0x100a0000]

    res = ram.cmd(" writeuart 'bu b u\\r\\n'")
    assert res == [0x13627520, 0x13622075, 0x120d0a00]

    res = ram.cmd(" writeuart acc , hex1")
    assert res == 0x17000000

    res = ram.cmd(" writeuart acc , hex3")
    assert res == 0x15000000

    res = ram.cmd(" jump #13")
    assert res == 0x2000000d

    res = ram.cmd(" loop #13")
    assert res == 0x2f00000d

    res = ram.cmd(" jump acc")
    assert res == 0x2e000000

    res = ram.cmd(" jump #13,rx_rdy")
    assert res == 0x2100000d

    res = ram.cmd(" jump #13,!rx_rdy")
    assert res == 0x2200000d

    res = ram.cmd(" jump #0x13")
    assert res == 0x20000013

    res = ram.cmd(" read uart")
    assert res == 0x30000000

    res = ram.cmd(" write uart")
    assert res == 0x40000000

    res = ram.cmd(" write @idx2+")
    assert res == 0x49000000

    res = ram.cmd(" write @4532")
    assert res == 0x4a0011b4

    res = ram.cmd(" read @4532")
    assert res == 0x3a0011b4

    res = ram.cmd(" read #4532")
    assert res == 0x3e0011b4

    res = ram.cmd(" read #0x123456")
    assert res == 0x3e123456

    res = ram.cmd(" read #0x3123456")
    assert res == [0x3e123456, 0x3f000003]

    ram.pc = 22
    res = ram.cmd(" jump $33,!rx_rdy")
    assert res == 0x22000000
    assert ram.backrefs['33'] == [22]
    ram.append(res)

    res = ram.cmd(" 33:")
    assert res == []
    assert ram.labels == {'33': 23}
    assert ram.data[22] == 0x22000017

    res = ram.cmd(" jump $33,!rx_rdy")
    assert res == 0x22000017

    res = ram.cmd(" ")
    assert res == []

    res = ram.cmd("          // comment ")
    assert res == []

    res = ram.cmd(" read #0x123456 // comment")
    assert res == 0x3e123456

    res = ram.cmd(" readwb @3")
    assert res == 0x18000003

    res = ram.cmd(" writewb @3")
    assert res == 0x19000003

    res = ram.cmd(" readdram @3")
    assert res == 0x1a000003

    res = ram.cmd(" writedram @3")
    assert res == 0x1b000003

    res = ram.cmd(" readdram @idx")
    assert res == 0x1c000000

    res = ram.cmd(" readdram @idx+")
    assert res == 0x1e000000

    res = ram.cmd(" writedram @idx2")
    assert res == 0x1d000000

    res = ram.cmd(" writedram @idx2+")
    assert res == 0x1f000000

    res = ram.cmd(" skip =3")
    assert res == 0x25000003

    res = ram.cmd(" skip !3")
    assert res == 0x26000003

    res = ram.cmd(" read r0")
    assert res == 0x34000000

    res = ram.cmd(" read r1")
    assert res == 0x35000000

    res = ram.cmd(" write r0")
    assert res == 0x44000000

    res = ram.cmd(" write r1")
    assert res == 0x45000000

    res = ram.cmd(" addh #0x2341")
    assert res == 0x51702341

    res = ram.cmd(" shift left8")
    assert res == 0x50100000

    res = ram.cmd(" shift right1")
    assert res == 0x50200000

    res = ram.cmd(" add r3")
    assert res == 0x52f00000

    res = ram.cmd(" add r2")
    assert res == 0x52e00000

    res = ram.cmd(" sub r2")
    assert res == 0x51e00000

    #print "assert res ==",dump_res(res)

    ram = Ram()

    src = open("prg.asm").read()

    for s in src.splitlines():
        ram.append(ram.cmd(s))

    ram.dump()
    
if __name__ == "__main__":
    test()
