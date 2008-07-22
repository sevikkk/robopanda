#!/usr/local/bin/python

class EmulationError(Exception):
    pass

class Decode_Result:
    def __init__(self, cmd, args = None, cmd_len = 1, descr = None, executor = None, next_addrs = None, barrier = 0, xrefs = [], exec_data = None, exec_cmd = None):
        self.cmd = cmd               # command name
        self.exec_cmd = exec_cmd               # command name
        self.args = args             # command arguments
        self.cmd_len = cmd_len       # command length in words
        self.descr = descr           # description of command (f.e.: "pop and compare", "branch if flag0")
        self.executor = executor     # description of command (f.e.: "pop and compare", "branch if flag0")
        self.exec_data = exec_data   # decoded data for execution
        self.next_addrs = next_addrs # possible start addresses of next commands other than pc + cmd_len
        self.barrier = barrier       # pc + cmd_len is not necessarily code
        self.xrefs = xrefs           # cross refs

class Execute_Result:
    def __init__(self, action = None, state = None, time = 0.05):
        self.action = action   # action executed in this cycle (f.e.: "$0 = 0x13", "@45 = 0x45")
        self.time = time   # time to next cycle ("m" - wait for mover, "p" - wait for player)
        self.state = state


class CPU_State:
    def __init__(self, clone_from = None):
        if not clone_from:
            self.stack = []
            self.pc = 0
            self.globals = {}
            self.locals = {}
            self.locals_offset = 0
            self.flag_f0 = False
            self.flag_e8 = False
            nvram_dump = """
0000: 3E 8D 37 88  22 CD 23 CD  67 AA 6A AB  5D 94 5A A1 
0010: 81 81 3B 00  B8 08 82 66  7A 48 44 44  38 5C 60 A6 
0020: FF 00 00 00  07 01 00 00  00 00 00 00  00 00 00 00 
0030: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 A6 00 
0040: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0050: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0060: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0070: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0080: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0090: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00A0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00B0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00C0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00D0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00E0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
00F0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0100: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0110: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0120: AA 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0130: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0140: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0150: 00 00 00 00  00 00 00 00  00 00 00 E6  FF 00 00 00 
0160: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
0170: 3E 8D 37 88  22 CD 23 CD  67 AA 6A AB  5D 94 5A A1 
0180: FF FF FF FF  FF FF 82 66  7A 48 44 44  38 5C 60 FF 
0190: 3E 8D 37 88  22 CD 23 CD  67 AA 6A AB  5D 94 5A A1 
01A0: 81 81 3B 00  B8 08 82 66  7A 48 44 44  38 5C 60 A6 
01B0: FF 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
01C0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
01D0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
01E0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
01F0: 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 
"""
            nvram = []
            for v in nvram_dump.split():
                if v.endswith(":"):
                    continue
                nvram.append(int(v,16))

            self.nvram = nvram
        else:
            old = clone_from
            self.stack = old.stack[:]
            self.pc = old.pc
            self.globals = old.globals.copy()
            self.locals = old.locals.copy()
            self.locals_offset = old.locals_offset
            self.nvram = old.nvram[:]

class CPU:
    bytecodes = [
            [ 0x0000, 0xFE00, "push_imm" ],
            [ 0x0200, 0xFF00, "and_imm" ],
            [ 0x0300, 0xFF00, "or_imm" ],
            [ 0x0400, 0xFF00, "xor_imm" ],
            [ 0x0500, 0xFF00, "mod_imm" ],
            [ 0x0600, 0xFF00, "add_imm" ],
            [ 0x0700, 0xFF00, "sub_imm" ],
            [ 0x0800, 0xFF00, "mul_imm" ],
            [ 0x0900, 0xFF00, "div_imm" ],
            [ 0x0A00, 0xFF00, "cmp_eq" ],
            [ 0x0B00, 0xFF00, "cmp_ne" ],
            [ 0x0C00, 0xFF00, "cmp_gt" ],
            [ 0x0D00, 0xFF00, "cmp_ge" ],
            [ 0x0E00, 0xFF00, "cmp_lt" ],
            [ 0x0F00, 0xFF00, "cmp_le" ],
            #1000
            #...
            #1F00
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
            [ 0x2960, 0xFFF0, "alu" ],
            [ 0x2978, 0xFFFF, "return" ],
            [ 0x2979, 0xFFFF, "return_if1" ],
            [ 0x297E, 0xFFFF, "drop" ],
            #2A00
            [ 0x2B00, 0xFF00, "alu_local" ],
            #2C00
            [ 0x2D00, 0xFF80, "push_local" ],
            [ 0x2D80, 0xFF80, "pop_local" ],
            [ 0x2EC0, 0xFFF0, "inc_local" ],
            #2F00
            #...
            [ 0x8500, 0xFF00, "cmp_local_ne" ],
            [ 0x9500, 0xFF00, "cmp_local" ],
            #A700
            [ 0xA800, 0xFC00, "set_local" ],
            [ 0xB000, 0xF000, "spi_read" ],
            [ 0xC000, 0xE000, "call" ],
            [ 0xE000, 0xF800, "rjump" ],
            [ 0xE800, 0xF800, "rjump_if1" ],
            [ 0xF000, 0xF800, "rjump_if0" ],
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

    def fetch(self, pc):
        return self.c.read_int16(pc * 2 + self.ib)

    def fetch_next(self, offset = 0):
        return self.c.read_int16((self.state.pc + offset) * 2 + self.ib)

    def format_addr(self, addr):
        if addr in self.labels:
            addr = self.labels[addr]
        else:
            addr = "%04X" % addr

        return addr

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
        res = decoder(cmd)
        res.exec_cmd = cmd_txt
        return res

    def execute(self, decoded, hint = None):
        state = CPU_State(self.state)
        state.pc += decoded.cmd_len

        if decoded.executor:
            executor = decoded.executor
        else:
            executor = getattr(self, "execute_" + decoded.exec_cmd)

        result = executor(decoded, state, hint)

        self.state = result.state

        return result

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

    def execute_push_imm(self, decoded, state, hint):

        val = decoded.exec_data

        state.stack.append(val)

        return Execute_Result(
                action = "push #%04X" % (val, ),
                state = state
            )

    def decode_and_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "and",
                "#%02X" % arg,
                descr = "stack AND arg",
                exec_data = arg,
            )

    def execute_and_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg & val)

        return Execute_Result(
                action = "stack & #%02X?" % (val,),
                state = state
            )

    def decode_or_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "or",
                "#%02X" % arg,
                descr = "stack OR arg",
                exec_data = arg,
            )

    def execute_or_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg | val)

        return Execute_Result(
                action = "stack | #%02X?" % (val,),
                state = state
            )

    def decode_xor_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "xor",
                "#%02X" % arg,
                descr = "stack XOR arg",
                exec_data = arg,
            )

    def execute_xor_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg ^ val)

        return Execute_Result(
                action = "stack ^ #%02X?" % (val,),
                state = state
            )

    def decode_mod_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "mod",
                "#%02X" % arg,
                descr = "stack % arg",
                exec_data = arg,
            )

    def execute_mod_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data

        if val != 0:
            state.stack.append( arg % val)
        else:
            state.stack.append(arg)

        return Execute_Result(
                action = "stack % #%02X?" % (val,),
                state = state
            )

    def decode_add_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "add",
                "#%02X" % arg,
                descr = "stack + arg",
                exec_data = arg,
            )

    def execute_add_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg + val)

        return Execute_Result(
                action = "stack + #%02X?" % (val,),
                state = state
            )

    def decode_sub_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "sub",
                "#%02X" % arg,
                descr = "stack - arg",
                exec_data = arg,
            )

    def execute_sub_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg - val)

        return Execute_Result(
                action = "stack - #%02X?" % (val,),
                state = state
            )

    def decode_mul_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "mul",
                "#%02X" % arg,
                descr = "stack * arg",
                exec_data = arg,
            )

    def execute_mul_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        state.stack.append( arg * val)

        return Execute_Result(
                action = "stack * #%02X?" % (val,),
                state = state
            )

    def decode_div_imm(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "div",
                "#%02X" % arg,
                descr = "stack / arg",
                exec_data = arg,
            )

    def execute_div_imm(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if val > 0:
            state.stack.append( arg / val)
        else:
            state.stack.append(0) 

        return Execute_Result(
                action = "stack / #%02X?" % (val,),
                state = state
            )

    def decode_cmp_eq(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_eq",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_eq(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg == val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack == #%02X?" % (val,),
                state = state
            )

    def decode_cmp_ne(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_ne",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_ne(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg != val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack != #%02X?" % (val,),
                state = state
            )

    def decode_cmp_gt(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_gt",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_gt(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg > val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack > #%02X?" % (val,),
                state = state
            )

    def decode_cmp_ge(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_ge",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_ge(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg >= val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack >= #%02X?" % (val,),
                state = state
            )

    def decode_cmp_lt(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_lt",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_lt(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg < val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack < #%02X?" % (val,),
                state = state
            )

    def decode_cmp_le(self, cmd):
        arg = cmd & 0xFF

        return Decode_Result(
                "cmp_le",
                "#%02X" % arg,
                descr = "pop value from stack and compare with arg",
                exec_data = arg,
            )

    def execute_cmp_le(self, decoded, state, hint):
        arg = state.stack.pop()
        val = decoded.exec_data
        if arg <= val:
            state.stack.append(1)
        else:
            state.stack.append(0)

        return Execute_Result(
                action = "stack <= #%02X?" % (val,),
                state = state
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

    def execute_push_glbl(self, decoded, state, hint):

        reg = decoded.exec_data

        val = state.globals[reg]
        state.stack.append(val)

        return Execute_Result(
                action = "push @%04X(#%04X)" % (reg, val),
                state = state
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

    def execute_pop_glbl(self, decoded, state, hint):

        arg = state.stack.pop()
        addr = decoded.exec_data
        state.globals[addr] = arg

        return Execute_Result(
                action = "@%04X = #%04X" % (addr, arg),
                state = state
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

    def execute_pop_glbl_offs(self, decoded, state, hint):

        arg = state.stack.pop()
        val = state.stack.pop()
        addr = decoded.exec_data
        state.globals[addr + arg] = val

        return Execute_Result(
                action = "@%04X = #%04X" % (addr + arg, val),
                state = state
            )

    def decode_expand(self, cmd):
        return Decode_Result(
                "expand",
                descr = "push 0 to stack (???)",
            )

    def execute_expand(self, decoded, state, hint):

        state.stack.append(0)

        return Execute_Result(
                action = "push #0",
                state = state
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

    def execute_nvram_read(self, decoded, state, hint):

        addr = state.stack.pop()

        if addr >= 0 and addr<len(state.nvram):
            val = state.nvram[addr]
        else:
            val = 255

        state.stack.append(val)
        
        return Execute_Result(
                action = "push nvram[%04X] (%04X)" % (addr, val),
                state = state
            )

    def decode_move(self, cmd):
        return Decode_Result(
                "move",
                descr = "pop mover script index from stack and start moving",
            )

    def decode_alu(self, cmd):
        op = [
                ("and", lambda x,y: x & y ),
                ("or", lambda x,y: x | y ),
                ("xor", lambda x,y: x ^ y ),
                ("mod", lambda x,y: x % y ),
                ("add", lambda x,y: x + y ),
                ("sub", lambda x,y: x - y ),
                ("mul", lambda x,y: x * y ),
                ("div", lambda x,y: x / y ),
                ("cmp_eq", lambda x,y: x == y ),
                ("cmp_ne", lambda x,y: x != y ),
                ("cmp_gt", lambda x,y: x > y ),
                ("cmp_ge", lambda x,y: x >= y ),
                ("cmp_lt", lambda x,y: x < y ),
                ("cmp_le", lambda x,y: x <= y ),
                ("shl", lambda x,y: x >> y ),
                ("shr", lambda x,y: x << y )
             ][cmd & 15]

        return Decode_Result(
                op[0],
                descr = "pop two args from stack and push result",
                exec_data = op[1],
            )

    def execute_alu(self, decoded, state, hint):

        arg2 = state.stack.pop()
        arg1 = state.stack.pop()
        result = decoded.exec_data(arg1, arg2)
        if decoded.cmd.startswith("cmp_"):
            if result:
                result = 1
            else:
                result = 0

        state.stack.append(result)
        
        return Execute_Result(
                action = "do op with stack",
                state = state
            )

    def decode_return(self, cmd):
        return Decode_Result(
                "return",
                descr = "pop return addr from stack, pop locals from stack, and continue from return addr",
                barrier = 1,
                executor = self.execute_return_if1
            )

    def decode_return_if1(self, cmd):
        return Decode_Result(
                "return_if1",
                descr = "check flag and return",
            )

    def execute_return_if1(self, decoded, state, hint):
        if decoded.exec_cmd == "return":
            do = True
            action = "return"
        elif decoded.exec_cmd == "return_if1":
            arg = state.stack.pop()
            do = arg & 1
            if do:
                action = "return_if1 (taken)"
            else:
                action = "return_if1 (not taken)"

        if do:
            npc = state.stack.pop() - self.ib/2

            mods = self.fetch(npc)
            nargs = mods >> 8
            nlocals = mods & 0xff

            state.locals_offset -= nlocals # save locals

            npc += 1
            state.pc = npc

        return Execute_Result(
                action = action,
                state = state
            )

    def decode_drop(self, cmd):
        return Decode_Result(
                "drop",
                descr = "pop and drop value from stack",
            )

    def execute_drop(self, decoded, state, hint):

        state.stack.pop()

        return Execute_Result(
                action = "drop",
                state = state
            )

    def decode_alu_local(self, cmd):

        op = cmd & 0xE0
        op = {
                0x00: "repli", # replace with immediate
                0x20: "addi",  # add immediate
                0x40: "and",
                0x60: "or",
                0x80: "xor",
                0xA0: "mod",
                0xC0: "add",
                0xE0: "sub",
            }[op]

        reg = cmd & 0x1F

        if op == 'addi':
            return Decode_Result(
                op,
                "#%02X" % (reg,),
                descr = "add #%02X to stack top " % (reg, ),
                exec_data = (op, reg),
            )
        elif op == 'repli':
            return Decode_Result(
                op,
                "#%02X" % (reg,),
                descr = "replace top of stack with #%02X" % (reg, ),
                exec_data = (op, reg),
            )
        else:
            return Decode_Result(
                op,
                "$%02X" % (reg,),
                descr = "%s local $%02X with stack and put result to stack" % (op, reg),
                exec_data = (op, reg),
            )

    def decode_push_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "push",
                "$%02X" % (arg,),
                descr = "push local $%02X to stack" % (arg),
                exec_data = arg,
            )

    def execute_push_local(self, decoded, state, hint):

        reg = decoded.exec_data

        val = state.locals[reg + state.locals_offset]
        state.stack.append(val)

        return Execute_Result(
                action = "push $%02X(#%04X)" % (reg,val),
                state = state
            )

    def decode_pop_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "pop",
                "$%02X" % (arg,),
                descr = "pop local $%02X from stack" % (arg),
                exec_data = arg,
            )


    def execute_pop_local(self, decoded, state, hint):

        reg = decoded.exec_data

        val = state.stack.pop()
        state.locals[reg + state.locals_offset] = val

        return Execute_Result(
                action = "pop $%02X(#%04X)" % (reg,val),
                state = state
            )

    def decode_inc_local(self, cmd):

        arg = cmd & 0xF

        return Decode_Result(
                "inc",
                "$%02X" % (arg,),
                descr = "increment local $%02X and push old value to stack" % (arg),
                exec_data = arg,
            )

    def execute_inc_local(self, decoded, state, hint):

        reg = decoded.exec_data

        val = state.locals[reg + state.locals_offset]
        state.stack.append(val)
        val += 1
        state.locals[reg + state.locals_offset] = val

        return Execute_Result(
                action = "push #%04X, $%02X = #%04X" % (val - 1, reg, val),
                state = state
            )

    def decode_cmp_local_ne(self, cmd):

        reg = (cmd & 0xF0) >> 4
        arg = cmd & 0xF

        return Decode_Result(
                "cmp",
                "$%02X, !#%02X" % (reg, arg),
                descr = "? $%02X != %02X" % (reg, arg),
                exec_data = (reg, arg)
            )

    def decode_cmp_local(self, cmd):

        reg = (cmd & 0xF0) >> 4
        arg = cmd & 0xF

        return Decode_Result(
                "cmp",
                "$%02X, #%02X" % (reg, arg),
                descr = "? $%02X == %02X" % (reg, arg),
                exec_data = (reg, arg)
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

    def execute_set_local(self, decoded, state, hint):

        reg, arg = decoded.exec_data

        state.locals[reg + state.locals_offset] = arg

        return Execute_Result(
                action = "$%02X = #%04X" % (reg, arg),
                state = state
            )

    def decode_spi_read(self, cmd):

        cmd_len = 1
        arg = cmd & 0xFFF
        if arg == 0xFFF:
            arg = self.fetch_next(1)
            cmd_len = 2

        arg += self.cx_off

        return Decode_Result(
                "spi_read",
                "%04X+" % (arg),
                descr = "pop offset from stack, read data from spi rom and push to stack",
                exec_data = arg,
                cmd_len = cmd_len,
                xrefs = [("data", arg)],
            )

    def execute_spi_read(self, decoded, state, hint):

        arg = state.stack.pop()
        addr = decoded.exec_data + arg

        val = self.fetch(addr)
        state.stack.append(val)
        
        return Execute_Result(
                action = "push rom[%04X] (%04X)" % (addr, val),
                state = state
            )

    def decode_call(self, cmd):

        cmd_len = 1
        addr = cmd & 0x1FFF

        if addr == 0x1FFF:
            addr = self.fetch_next(1)
            cmd_len += 1

        addr += self.cx_off

        mods = self.fetch_next(cmd_len)
        cmd_len += 1

        nargs = mods >> 8
        nlocals = mods & 0xff

        return Decode_Result(
                "call",
                "%s(%d,%d)" % (self.format_addr(addr), nargs, nlocals),
                descr = "save %d locals and call %04X with %d args from stack)" % (nlocals, addr, nargs),
                exec_data = (addr, nargs, nlocals),
                cmd_len = cmd_len,
                next_addrs = [addr],
                xrefs = [("code_global", addr)],
            )

    def execute_call(self, decoded, state, hint):

        addr, nargs, nlocals = decoded.exec_data

        ret = state.pc - 1

        state.locals_offset += nlocals # save locals

        args = state.stack[:nargs] # pop args
        state.stack = state.stack[nargs:]

        state.stack.append(ret + self.ib/2) # push return address
        state.stack += args  # push args

        state.pc = addr
        return Execute_Result(
                action = "call %04X(%s)" % (addr, ",".join(["%s" % a for a in args])),
                state = state
            )

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

    def execute_rjump(self, decoded, state, hint):

        addr = decoded.exec_data

        state.pc = addr

        return Execute_Result(
                action = "jump %04X" % (addr, ),
                state = state
            )

    def decode_rjump_if1(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 1

        return Decode_Result(
                "rjump_if1",
                "%s" % (self.format_addr(addr)),
                descr = "pop and conditional jump to %04X" % (addr,),
                exec_data = addr,
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
            )

    def execute_rjump_if1(self, decoded, state, hint):

        addr = decoded.exec_data
        arg = state.stack.pop()
        do = arg & 1
        if do:
            state.pc = addr
            action = "taken"
        else:
            action = "not taken"

        return Execute_Result(
                action = "jump %04X (%s)" % (addr, action),
                state = state
            )

    def decode_rjump_if0(self, cmd):
        offset = (cmd & 0x7FF)
        if offset & 0x400 != 0:
            offset = offset - 0x801

        addr = self.state.pc + offset + 1

        return Decode_Result(
                "rjump_if0",
                "%s" % (self.format_addr(addr)),
                descr = "pop and conditional jump to %04X" % (addr,),
                exec_data = addr,
                xrefs = [("code_local", addr)],
                next_addrs = [addr],
            )

    def execute_rjump_if0(self, decoded, state, hint):

        addr = decoded.exec_data
        arg = state.stack.pop()
        do = not (arg & 1)
        if do:
            state.pc = addr
            action = "taken"
        else:
            action = "not taken"

        return Execute_Result(
                action = "jump %04X (%s)" % (addr, action),
                state = state
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

    def dump_stack(self):
        s = []
        st = self.state.stack[:]
        st.reverse()
        for a in st:
            s.append("%04X" % a)

        return "[" + ",".join(s) + "]"

    def do_one_cmd(self, ts, real_addr):
        real_pc = (real_addr - self.ib)/2
        if self.state.pc != real_pc:
            print "[ERROR] pc != real_pc: %06X != %06X" % (self.state.pc, real_pc)

        assert self.state.pc == real_pc

        hint = None
        decoded = self.decode()
        execed = self.execute(decoded, hint)
        print "%9.3f %06X [CPU] %06X: %-9s %-20s // %s, stack: %s" % (ts, real_addr, real_pc, decoded.cmd, decoded.args or "", execed.action or "", self.dump_stack())
            
    def bubu(self):
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
