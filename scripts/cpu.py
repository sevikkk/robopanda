#!/usr/local/bin/python

class EmulationError(Exception):
    pass

class Decode_Result:
    def __init__(self, cmd, args = None, cmd_len = 1, descr = None, executor = None, next_addrs = None, barrier = 0, xrefs = [], exec_data = None):
        self.cmd = cmd               # command name
        self.args = args             # command arguments
        self.cmd_len = cmd_len       # command length in words
        self.descr = descr           # description of command (f.e.: "pop and compare", "branch if flag0")
        self.executor = executor     # description of command (f.e.: "pop and compare", "branch if flag0")
        self.exec_data = exec_data   # decoded data for execution
        self.next_addrs = next_addrs # possible start addresses of next commands other than pc + cmd_len
        self.barrier = barrier       # pc + cmd_len is not necessarily code
        self.xrefs = xrefs           # cross refs

class Execute_Result:
    def __init__(self, npc = None, action = None, state = None):
        self.action = action   # action executed in this cycle (f.e.: "$0 = 0x13", "@45 = 0x45")
        self.npc = npc         # new value of pc for branches/calls (if not pc + len)
        self.state = state     # new state of cpu (locals, globals, stack, etc)

class CPU_State:
    def __init__(self, clone_from = None):
        if not clone_from:
            self.stack = []
            self.pc = 0
            self.globals = {}
            self.locals = {}
            self.locals_offset = 0
        else:
            old = clone_from
            self.stack = old.stack[:]
            self.pc = old.pc
            self.globals = old.globals.copy()
            self.locals = old.locals.copy()
            self.locals_offset = old.locals_offset

class CPU:
    bytecodes = [
            [ 0x0000, 0xFE00, "push_imm" ],
            [ 0x0E00, 0xFF00, "cmp" ],
            [ 0x2000, 0xFF00, "push_glbl" ],
            [ 0x2100, 0xFF00, "push_glbl_offs" ],
            #2200
            #2300
            [ 0x2400, 0xFF00, "pop_glbl" ],
            [ 0x2500, 0xFF00, "pop_glbl_offs" ],
            #2600
            #2700
            #2800
            [ 0x2902, 0xFFFF, "expand" ],
            [ 0x2912, 0xFFFF, "gpio" ],
            [ 0x291A, 0xFFFF, "volume" ],
            [ 0x2923, 0xFFFF, "wait_play" ],
            [ 0x2928, 0xFFFF, "play" ],
            [ 0x2929, 0xFFFF, "nvram_write" ],
            [ 0x292A, 0xFFFF, "nvram_read" ],
            [ 0x292F, 0xFFFF, "move" ],
            [ 0x2978, 0xFFFF, "return" ],
            [ 0x2979, 0xFFFF, "return_f0" ],
            [ 0x297E, 0xFFFF, "drop" ],
            #2A00
            #2B00
            [ 0x2D00, 0xFF80, "push_local" ],
            [ 0x2D80, 0xFF80, "pop_local" ],
            [ 0x2EC0, 0xFFF0, "inc_local" ],
            #2F00
            #...
            #A700
            [ 0xA800, 0xFC00, "set_local" ],
            [ 0xB000, 0xF000, "spi_read" ],
            [ 0xC000, 0xE000, "call" ],
            [ 0xE000, 0xF800, "rjump" ],
            [ 0xE800, 0xF800, "rjump_e8" ],
            [ 0xF000, 0xF800, "rjump_f0" ],
            [ 0xF800, 0xF800, "rjump_arg" ],
    ]

    def __init__(self, cartridge, index_base, cmdCX_offset, start, mover, player):
        self.c = cartridge
        self.ib = index_base
        self.cx_off = cmdCX_offset
        self.mover = mover
        self.player = player

        self.state = CPU_State()
        self.state.pc = start
        self.alt_state = None

        self.labels = {}

    def decode(self, pc = None):
        if pc is not None:
            self.state.pc = pc # for disassembler and likes

        cmd = self.fetch_next()
        cmd_txt = "unknown"
        for val, mask, txt in self.bytecodes:
            if cmd & mask == val:
                cmd_txt = txt
                break

        decoder = getattr(self, "decode_" + cmd_txt)
        return decoder(cmd)

    def decode_push_imm(self, cmd):

        cmd_len = 1
        arg = cmd & 0x1FF

        if arg == 0x1FF:
            arg = self.fetch_next(1)
            cmd_len += 1

        return Decode_Result(
                "push",
                "#%04X" % (arg,),
                descr = "push %04X to stack" % (arg),
                exec_data = arg,
                cmd_len = cmd_len,
            )

    def decode_cmp(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def decode_push_glbl(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFF

        if arg == 0xFF:
            arg = self.fetch_next(1)
            cmd_len += 1

        return Decode_Result(
                "push",
                "@%04X" % (arg,),
                descr = "push global %04X to stack" % (arg),
                exec_data = arg,
                xrefs = [("globals", arg)],
                cmd_len = cmd_len,
            )

    def decode_push_glbl_offs(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFF

        if arg == 0xFF:
            arg = self.fetch_next(1)
            cmd_len += 1

        return Decode_Result(
                "push",
                "@%04X+" % (arg,),
                descr = "pop offset from stack, and push global %04X+offset to stack" % (arg),
                exec_data = arg,
                xrefs = [("globals", arg)],
                cmd_len = cmd_len,
            )

    def decode_pop_glbl(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFF

        if arg == 0xFF:
            arg = self.fetch_next(1)
            cmd_len += 1

        return Decode_Result(
                "pop",
                "@%04X" % (arg,),
                descr = "pop global %04X from stack" % (arg),
                exec_data = arg,
                xrefs = [("globals", arg)],
                cmd_len = cmd_len,
            )

    def decode_pop_glbl_offs(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFF

        if arg == 0xFF:
            arg = self.fetch_next(1)
            cmd_len += 1

        return Decode_Result(
                "pop",
                "@%04X+" % (arg,),
                descr = "pop offset from stack, pop global %04X+offset from stack" % (arg),
                exec_data = arg,
                xrefs = [("globals", arg)],
                cmd_len = cmd_len,
            )

    def decode_expand(self, cmd):
        return Decode_Result(
                "expand",
                descr = "push 0 to stack (???)",
            )

    def decode_gpio(self, cmd):
        return Decode_Result(
                "gpio",
                descr = "pop gpio outs from stack",
            )

    def decode_volume(self, cmd):
        return Decode_Result(
                "volume",
                descr = "pop volume from stack",
            )

    def decode_wait_play(self, cmd):
        return Decode_Result(
                "wait_play",
                descr = "wait for and of play",
            )

    def decode_play(self, cmd):
        return Decode_Result(
                "play",
                descr = "pop audio index from stack and start play",
            )

    def decode_nvram_write(self, cmd):
        return Decode_Result(
                "nvram_write",
                descr = "pop nvram addres and value from stack and write it",
            )

    def decode_nvram_read(self, cmd):
        return Decode_Result(
                "nvram_read",
                descr = "pop nvram addres from stack, read and put result on stack",
            )

    def decode_move(self, cmd):
        return Decode_Result(
                "move",
                descr = "pop mover script index from stack and start moving",
            )

    def decode_return(self, cmd):
        return Decode_Result(
                "return",
                descr = "pop return addr from stack, pop locals from stack, and continue from return addr",
                barrier = 1
            )

    def decode_return_f0(self, cmd):
        return Decode_Result(
                "return_f0",
                descr = "check flag and return",
            )

    def decode_drop(self, cmd):
        return Decode_Result(
                "drop",
                descr = "pop and drop value from stack",
            )

    def decode_push_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "push",
                "$%02X" % (arg,),
                descr = "push local %02X to stack" % (arg),
                exec_data = arg,
            )

    def decode_pop_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "pop",
                "$%02X" % (arg,),
                descr = "pop local %02X from stack" % (arg),
                exec_data = arg,
            )

    def decode_inc_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "inc",
                "$%02X" % (arg,),
                descr = "increment local %02X and push old value to stack" % (arg),
                exec_data = arg,
            )

    def decode_set_local(self, cmd):

        arg = cmd & 0x3F
        reg = (cmd >> 6)& 0x7

        return Decode_Result(
                "set",
                "$%02X, #%02X" % (reg, arg),
                descr = "set local %02X to %02X" % (reg, arg),
                exec_data = (reg, arg)
            )

    def decode_spi_read(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFFF
        if arg == 0xFFF:
            arg = self.fetch_next(1)
            cmd_len = 2

        return Decode_Result(
                "spi_read",
                "%04X+" % (arg),
                descr = "pop offset from stack, read data from spi rom and push to stack",
                exec_data = arg,
                cmd_len = cmd_len,
                xrefs = [("data", arg)],
            )

    def decode_call(self, cmd):

        result = Decode_Result("call")

        addr = cmd & 0x1FFF

        if addr == 0x1FFF:
            addr = self.fetch_next(1)
            result.cmd_len += 1

        addr += self.cx_off

        mods = self.fetch_next(result.cmd_len)
        result.cmd_len += 1

        nargs = mods >> 8
        nlocals = mods & 0xff

        result.exec_data = (addr, nargs, nlocals)
        result.args = "%s(%d,%d)" % (self.format_addr(addr), nargs, nlocals)
        result.descr = "save %d locals and call %04X with %d args from stack)" % (nlocals, addr, nargs)
        result.next_addrs = [addr]
        result.xrefs = [("code_global", addr)]
        return result

    def execute_call(self, cmd, new_state):
        pc = self.state.pc

        addr = cmd & 0x1FFF
        if addr == 0x1FFF:
            addr = self.fetch(pc + 1)
            statepc += 1

        ret = npc

        mods = self.fetch(npc)
        nargs = mods >> 8
        nlocals = mods & 0xff

        self.locals_offset += nlocals # save locals

        args = self.stack[:nargs] # pop args
        self.stack = self.stack[nargs:]

        self.stack.append(ret + self.ib/2) # push return address
        self.stack += args  # push args

        npc = addr + self.cx_off
        result = Cmd_Result()
        print "%9.3f %06X [CPU] %06X: call %04X // stack: %s" % (ts, real_addr, pc, npc, self.dump_stack())

    def format_addr(self, addr):
        if addr in self.labels:
            addr = self.labels[addr]
        else:
            addr = "%04X" % addr

        return addr

    def decode_rjump(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 1

        return Decode_Result(
                "rjump",
                "%s" % (self.format_addr(addr)),
                descr = "jump to %04X" % (addr,),
                exec_data = addr,
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
                barrier = 1,
            )

    def decode_rjump_e8(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 1

        return Decode_Result(
                "rjump_e8",
                "%s" % (self.format_addr(addr)),
                descr = "conditional jump to %04X" % (addr,),
                exec_data = addr,
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
            )

    def decode_rjump_f0(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 1

        return Decode_Result(
                "rjump_f0",
                "%s" % (self.format_addr(addr)),
                descr = "conditional jump to %04X" % (addr,),
                exec_data = addr,
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
            )

    def decode_rjump_arg(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 2
        arg = self.fetch_next(1)

        return Decode_Result(
                "rjump_neq",
                "%s,%04X" % (self.format_addr(addr), arg),
                descr = "if value on stack != %04X, jump to %04X, else pop, drop and continue" % (arg, addr,),
                exec_data = (addr, arg),
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
                cmd_len = 2
            )

    def decode_unknown(self, cmd):

        args = "%04X" % (cmd,)
        result = Decode_Result("unknown", args)
        return result

    def fetch(self, pc):
        return self.c.read_int16(pc * 2 + self.ib)

    def fetch_next(self, offset = 0):
        return self.c.read_int16((self.state.pc + offset) * 2 + self.ib)

    def dump_stack(self):
        s = []
        st = self.stack[:]
        st.reverse()
        for a in st:
            s.append("%04X" % a)

        return "[" + ",".join(s) + "]"

    def do_one_cmd(self, ts, real_addr):
        real_pc = (real_addr - self.ib)/2
        if self.pc != real_pc:
            #print "[WARNING] pc != real_pc: %06X != %06X" % (self.pc, real_pc)
            #try:
            #    print "alt_branch: %06X" % self.alt_branch
            #except:
            #    print "alt_branch: %s" % self.alt_branch
            if self.alt_branch == real_pc:
                self.pc = self.alt_branch
            
        self.alt_branch = None
        pc = self.pc
        npc = pc + 1

        cmd = self.fetch(pc)

        if cmd & 0xE000 == 0xC000:
            addr = cmd &0x1FFF
            if addr == 0x1FFF:
                addr = self.fetch(pc + 1)
                npc += 1

            ret = npc


            mods = self.fetch(npc)
            nargs = mods >> 8
            nlocals = mods & 0xff

            self.locals_offset += nlocals # save locals

            args = self.stack[:nargs] # pop args
            self.stack = self.stack[nargs:]

            self.stack.append(ret + self.ib/2) # push return address
            self.stack += args  # push args

            npc = addr + self.cx_off
            print "%9.3f %06X [CPU] %06X: call %04X // stack: %s" % (ts, real_addr, pc, npc, self.dump_stack())
        elif cmd & 0xFC00 == 0xA800:
            reg = (cmd >> 6) & 0xF
            value = cmd & 0x3F
            self.locals[reg + self.locals_offset] = value
            print "%9.3f %06X [CPU] %06X: set $%X, #%02X // $%X = %02X" % (ts, real_addr, pc, reg, value, reg, value)
        elif cmd & 0xFE00 == 0x0000:
            arg = cmd & 0x1FF
            if arg == 0x1FF:
                arg = self.fetch(pc + 1)
                npc = pc + 2
            self.stack.append(arg)
            print "%9.3f %06X [CPU] %06X: push #%04X // stack: %s" % (ts, real_addr, pc, arg, self.dump_stack())
        elif cmd & 0xFFF0 == 0x2EC0:
            arg = cmd & 0xF
            old = self.locals[arg + self.locals_offset]
            self.locals[arg + self.locals_offset] = old + 1
            self.stack.append(old)
            print "%9.3f %06X [CPU] %06X: inc $%X // $%X = %04X, stack: %s" % (ts, real_addr, pc, arg, arg, old+1, self.dump_stack())
        elif cmd & 0xFF80 == 0x2D80:
            arg = cmd & 0x7F
            value = self.stack.pop()
            self.locals[arg + self.locals_offset] = value
            print "%9.3f %06X [CPU] %06X: pop $%X // $%X = %04X, stack: %s" % (ts, real_addr, pc, arg, arg, value, self.dump_stack())
        elif cmd & 0xFF80 == 0x2D00:
            arg = cmd & 0x7F
            self.stack.append(self.locals.get(arg + self.locals_offset,0))
            print "%9.3f %06X [CPU] %06X: push $%X // stack: %s" % (ts, real_addr, pc, arg, self.dump_stack())
        elif cmd & 0xF800 in (0xF000,0xE000, 0xE800):
            offset = (cmd & 0x7FF)

            if offset & 0x400 != 0:
                offset = offset - 0x801

            if cmd & 0xF800 in (0xF000, 0xE800):
                tc = "rjump_%x" % ((cmd&0xf800)>>8)

                addr = (self.c.orig_lookup() - self.ib)/2
                if addr == pc + offset + 1:
                    flag = 1
                else:
                    flag = 0

            if cmd & 0xF800 == 0xE000:
                flag = 1
                tc = "rjump"

            if flag:
                self.alt_branch = npc
                npc = pc + offset + 1
            else:
                self.alt_branch = pc + offset + 1

            print "%9.3f %06X [CPU] %06X: %s %06X" % (ts, real_addr, pc, tc, pc + offset + 1)
        elif cmd & 0xF800 == 0xF800:
            arg = self.fetch(pc + 1)
            offset = (cmd & 0x7FF)
            if offset & 0x400 != 0:
                offset = offset - 0x801

            addr = (self.c.orig_lookup() - self.ib)/2

            if addr == pc + offset + 2:
                flag = 1
            else:
                flag = 0

            if flag:
                self.alt_branch = pc + 2
                npc = pc + offset + 2
            else:
                self.alt_branch = pc + offset + 2
                npc = pc + 2

            print "%9.3f %06X [CPU] %06X: jump_arg %06X %06X" % (ts, real_addr, pc, arg, pc + offset + 2)

        elif cmd == 0x2902:
            arg = self.stack.pop()
            self.stack.append(arg)
            self.stack.append(0)
            print "%9.3f %06X [CPU] %06X: extend // stack: %s" % (ts, real_addr, pc, self.dump_stack())
        elif cmd == 0x297E:
            arg = self.stack.pop()
            print "%9.3f %06X [CPU] %06X: drop // stack: %s" % (ts, real_addr, pc, self.dump_stack())
        elif cmd == 0x2928:
            addr = self.c.orig_lookup()
            a1,a2,a3,a4 = self.c.read(addr,4)
            addr = a1 + 256 * a2 + 65536 * a3
            print "%9.3f %06X [CPU] %06X: play (%02X %06X)" % (ts, real_addr, pc, a4, addr)
            self.player.start(ts, addr)
        elif cmd == 0x292F:
            addr = (self.c.orig_lookup() - self.ib)/2
            if addr != npc:
                addr = self.fetch(addr)
                self.mover.start(ts, addr)
            else:
                print "[WARNING] conditional move?"

            print "%9.3f %06X [CPU] %06X: move (%06X)" % (ts, real_addr, pc, addr)
        elif cmd == 0x2979 or cmd == 0x2978:
            ret = self.stack[-1] - self.ib/2
            addr = (self.c.orig_lookup() - self.ib)/2
            if cmd == 0x2979:
                cmd = "return_f0"
                if addr == ret:
                    flag = 1
                else:
                    flag = 0
            else:
                cmd = "return"
                flag = 1

            if flag:
                npc = self.stack.pop() - self.ib/2

                mods = self.fetch(npc)
                nargs = mods >> 8
                nlocals = mods & 0xff

                self.locals_offset -= nlocals # save locals

                npc += 1
                
            print "%9.3f %06X [CPU] %06X: %s // stack: %s" % (ts, real_addr, pc, cmd, self.dump_stack())
        elif (cmd & 0xF000) == 0xB000:
            offset = cmd & 0xFFF
            if offset == 0xFFF:
                offset = self.fetch(pc + 1)
                npc = pc + 2
            arg = self.stack.pop()
            addr = (arg + offset + self.cx_off)*2 + self.ib
            value = self.c.read_int16(addr)
            self.stack.append(value)
            print "%9.3f %06X [CPU] %06X: readspi %04X // stack: %s" % (ts, real_addr, pc, offset, self.dump_stack())
        elif (cmd & 0xFF00) == 0x0E00:
            arg = cmd & 0xFF
            value = self.stack.pop()
            print "%9.3f %06X [CPU] %06X: cmp #%02X // %04X == %02X?, stack: %s" % (ts, real_addr, pc, arg, value, arg, self.dump_stack())
        elif (cmd & 0xFF00) == 0x2400:
            arg = cmd & 0xFF
            value = self.stack.pop()
            self.globals[arg] = value
            print "%9.3f %06X [CPU] %06X: pop @%02X // @%X = %04X, stack: %s" % (ts, real_addr, pc, arg, arg, value, self.dump_stack())
        elif (cmd & 0xFF00) == 0x2500:
            arg = cmd & 0xFF
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.globals[arg] = value1
            self.globals[arg+1] = value2
            print "%9.3f %06X [CPU] %06X: pop2 @%02X // @%X,@%X = %04X,%04X, stack: %s" % (ts, real_addr, pc, arg, arg, arg + 1, value1, value2, self.dump_stack())
        elif (cmd & 0xFF00) == 0x2000:
            arg = cmd & 0xFF
            value = self.globals.get(arg, 0)
            self.stack.append(value)
            print "%9.3f %06X [CPU] %06X: push @%02X // stack: %s" % (ts, real_addr, pc, arg, self.dump_stack())
        elif cmd == 0x0002:
            print "%9.3f %06X [CPU] %06X: nop" % (ts, real_addr, pc)
        else:
            print "%9.3f %06X [CPU] %06X: unknown %04X" % (ts, real_addr, pc, cmd)

        self.pc = npc
