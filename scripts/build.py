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
    mover_num = 5
    code = []
    mover = [0xF000]
    code_labels = {}
    mover_entries = {}
    refs = {}
    max_audio = 0

    for line in cfg:
        line = line[:-1]
        line = line.split("#")[0]
        line = line.split()
        if not line:
            continue

        if line[0] == "start":
            start = int(line[1],0)
        elif line[0] == "version":
            version = int(line[1],0)
        elif line[0] == "cx_offset":
            cx_offset = int(line[1],0)
        elif line[0] == "audio":
            label = int(line[1])
            assert label>0
            fname = line[2]
            audio[label] = fname
            max_audio = max(max_audio, label)
        elif line[0] == "code":
            for c in line[1:]:
                c = int(c,16)
                code.append(c)
        elif line[0] == "code_label":
            label = line[1]
            code_labels[label] = len(code)
        elif line[0] == "mover_entry":
            label = int(line[1])
            assert label>0
            mover_entries[label] = len(mover)
        elif line[0] == "mover":
            for c in line[1:]:
                c = int(c,16)
                mover.append(c)
        else:
            print "unparsed line:", " ".join(line)

    index = (max_audio + 1)*3 + 0x20
    index = (int(index + 0x100)/0x100)*0x100
    data = StringIO.StringIO()
    #data.seek(8*1024*1024-1)
    #data.write('\x00')
    data.seek(0)
    data.write('\xCC\xBB')
    data.write(struct.pack("<H",index))

    code_ptr = index + 0x40
    start = (code_ptr - index)/2
    mover_ptr = code_ptr + len(code)*2 + 2
    first_mover_ptr = mover_ptr + mover_num * 2
    first_move = (first_mover_ptr - index)/2
    version_ptr = mover_ptr + mover_num * 2 + len(mover)*2 + 2
    audio_ptr = int((version_ptr + 0x101)/0x100)*0x100
    data.seek(index)
    data.write('\x55\xAA')
    data.write(struct.pack("<H",(version_ptr - index)/2))
    data.write(struct.pack("<H",(mover_ptr - index)/2))
    data.write(struct.pack("<H",cx_offset))
    data.write(struct.pack("<H",start))

    mks = mover_entries.keys()
    mks.sort()
    mover_num = mks[-1]+1

    data.seek(mover_ptr - 2)
    data.write(struct.pack("<H",mover_num))
    addr = 0
    for a in range(0,mover_num):
        if a in mover_entries:
            addr = mover_entries[a]
        data.write(struct.pack("<H",first_move + addr))

    data.seek(first_mover_ptr)
    for c in mover:
        data.write(struct.pack("<H",c))

    data.seek(code_ptr)
    for c in code:
        data.write(struct.pack("<H",c))

    data.seek(version_ptr)
    data.write(struct.pack("<H",version))

    data.seek(audio_ptr)
    n = 1
    aidx = {}
    aks = audio.keys()
    aks.sort()
    for al in aks:
        afn = audio[al]
        adata = open(afn,'rb').read()
        aidx[al] = data.tell()
        data.write(struct.pack("<L", len(adata)+4))
        data.write(adata)

    aidx[al+1] = data.tell()
    data.write("\x00\x00\x00\x00")

    data.seek(5)
    addr = 0
    for a in range(1,al+2):
        if a in aidx:
            addr = aidx[a]
        data.write(struct.pack("<L", (addr))[:3])
    data.write("@PEND\x00")

    data.seek(0)

    open(result,"wb").write(data.read())

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
