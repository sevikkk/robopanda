#!/usr/local/bin/python
import StringIO
import struct

def main(config, result):
    cfg = open(config,"r").readlines()
    audio = {}
    index = 0x2000
    start = 0
    version = 2
    cx_offset = 0xC
    code_len = 0x100
    mover_len = 0x100
    mover_num = 5
    code = []
    mover = []
    labels = {}
    refs = {}

    for line in cfg:
        line = line[:-1]
        line = line.split("#")[0]
        line = line.split()
        if not line:
            continue

        if line[0] == "index":
            index = int(line[1],0)
        elif line[0] == "index":
            index = int(line[1],0)
        elif line[0] == "start":
            start = int(line[1],0)
        elif line[0] == "version":
            version = int(line[1],0)
        elif line[0] == "cx_offset":
            cx_offset = int(line[1],0)
        elif line[0] == "code_len":
            code_len= int(line[1],0)
        elif line[0] == "mover_len":
            mover_len= int(line[1],0)
        elif line[0] == "mover_num":
            mover_num= int(line[1],0)
        elif line[0] == "audio":
            label = line[1]
            fname = line[2]
            audio[label] = fname
        elif line[0] == "code":
            for c in line[1:]:
                c = int(c,16)
                code.append(c)
        elif line[0] == "mover":
            for c in line[1:]:
                c = int(c,16)
                mover.append(c)

    data = StringIO.StringIO()
    #data.seek(8*1024*1024-1)
    #data.write('\x00')
    data.seek(0)
    data.write('\xCC\xBB')
    data.write(struct.pack("<H",index))

    code_ptr = index + 0x40
    start = (code_ptr - index)/2
    mover_ptr = code_ptr + code_len*2 + 2
    first_mover_ptr = mover_ptr + mover_num * 2
    first_move = (first_mover_ptr - index)/2
    version_ptr = mover_ptr + mover_num * 2 + mover_len*2 + 2
    data.seek(index)
    data.write('\x55\xAA')
    data.write(struct.pack("<H",(version_ptr - index)/2))
    data.write(struct.pack("<H",(mover_ptr - index)/2))
    data.write(struct.pack("<H",cx_offset))
    data.write(struct.pack("<H",start))
    data.seek(mover_ptr - 2)
    data.write(struct.pack("<H",mover_num))
    data.write(struct.pack("<H",first_move))
    data.write(struct.pack("<H",first_move))
    data.write(struct.pack("<H",first_move))
    data.seek(first_mover_ptr)
    for c in mover:
        data.write(struct.pack("<H",c))

    data.seek(code_ptr)
    for c in code:
        data.write(struct.pack("<H",c))

    data.seek(version_ptr)
    data.write(struct.pack("<H",version))

    #data.seek(code_ptr)
    #data.write("\x02\x00\x02\x00\x02\x00")
    #data.seek(mover_ptr)
    #data.write("\x00\xF0\x00\xF0\x00\xF0")

    data.seek(0x10000)
    n = 1
    aidx = []
    for al, afn in audio.items():
        adata = open(afn,'r').read()
        aidx.append(data.tell())
        data.write(struct.pack("<L", len(adata)+4))
        data.write(adata)
    aidx.append(data.tell())
    data.write("\x00\x00\x00\x00")

    data.seek(5)
    for a in aidx:
        data.write(struct.pack("<L", (a))[:3])
    data.write("@PEND\x00")

    data.seek(0)

    open(result,"w").write(data.read())

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
