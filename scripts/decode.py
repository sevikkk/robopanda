#!/usr/local/bin/python

"""
 sox -V 02\ -\ Winnie-the-Pooh\ -\ Introduction.mp3 -c 1 -s -w test_encode_input.wav trim 0 60 stat
"""

import struct
import sys
import wave
import math
from numpy import array

class Meta:

    def __init__(self, frame_len):
        self.frame_len = frame_len

        self.freq_resp = {
            0:	5000,
            1:	4920,
            2:	4715,
            3:	4469,
            4:	4141,
            5:	3785,
            6:	3416,
            7:	3047,
            8:	2590,
            9:	2360,
            10:	2049,
            11:	1765,
            12:	1503,
            13:	1267,
            14:	1057,
            15:	871
        }

        self.main_volumes = []
        k = 1
        for i in range(15):
            self.main_volumes.append(k)
            k = k * 0.6
        self.main_volumes.append(0)
    
        self.local_volumes = [1.0]
        k = 0.75
        for i in range(7):
            self.local_volumes.append(k)
            if i<4:
                k = k * 0.75
            else:
                k = k * 0.6
        self.local_volumes.append(0)

        self.filter1 = array([0.0] * frame_len)
        self.filter2 = array([0.0] * frame_len)
        for i in range(frame_len):
            w = math.sin(math.pi/2*i/frame_len)
            self.filter1[i] = w
            self.filter2[frame_len-i-1] = w

meta = Meta(512)

class SubBand:
    def __init__(self, freq, phase):
        self.freq = freq
        self.phase = phase

        self.volume = 0
        self.inverse = 0
        self.format = "aaai"

    def decode(self, value):
        self.volume = value >> 1
        self.inverse = value & 1

    def encode(self):
        return self.volume << 1 | self.inverse

    def __str__(self):
        return "SubBand(freq=%.1f, phase=%d, volume=%d, inverse=%d)" % (
                self.freq, self.phase, self.volume,  self.inverse)

    def generate(self, frame):
        fi = self.phase*math.pi/180
        delta_fi = self.freq*2*math.pi*0.016/len(frame)

        k = meta.local_volumes[8 - self.volume]
        if self.inverse:
            k = -k

        k = -k # robopanda output is inverted

        for i in range(len(frame)):
            x = math.cos(fi) * k
            frame[i] += x
            fi += delta_fi

class Band:
    def __init__(self, band):
        self.band = band
        self.base_freq = band * 250.0

        self.subbands = []
        for freq, phase in [
                (0,   0), #0    500.0
                (1, 180), #1    562.5
                (1,  90), #2    562.5
                (2, -90), #3    625.0
                (2, 180), #4    625.0
                (3,   0), #5    687.5
                (3, -90), #6    687.5
                (4,  90), #7    750.0
                (4,   0), #8    750.0 (only in 2 nibbles format)
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))

        self.format = 0
        self.frame_offset = 0
        self.volume = 0
        self.main_subband = 0
        self.inverse = 0

    def str_subs(self):
        s = []
        if self.base_subband:
            s.append("\t"+str(self.base_subband)+"\n")
        return "".join(s)

    def __str__(self):
        s = ["Band(band = %d, freq=%.1f, volume=%d, main_sb=%d, inverse=%d, format=%d, frame_offset=%d [\n" % 
                (self.band, self.base_freq, self.volume, self.main_subband, 
                    self.inverse, self.format, self.frame_offset)]

        for i in range(9):
            if self.subbands[i].volume > 0:
                s.append("\t"+str(self.subbands[i])+"\n")

        s.append("]")

        return "".join(s)

    def encode(self, frame):
        frame[self.band] = self.volume
        for i in range(self.num_subs):
            frame[self.frame_offset+i] = self.subbands[i].encode()

    def decode(self, frame):
        self.volume = frame[self.band]

        if self.format == 8:
            subframe = frame[self.frame_offset:self.frame_offset+8] + [0]
        elif self.format == 6:
            subframe_packed = frame[self.frame_offset:self.frame_offset+6]
            subframe = subframe_packed[:4]
            subframe += [subframe_packed[4] & 3,subframe_packed[4]>>2]
            subframe += [subframe_packed[5] & 3,subframe_packed[5]>>2]
            subframe += [0]
            for b in range(4,8):
                if b <= self.main_subband:
                    subframe[b] = subframe[b]<<2 # ia -> ia00
                else:
                    subframe[b] = ((subframe[b] & 2) << 2) | (subframe[b] & 1) # ai -> a00i
        elif self.format == 2:
            subframe = [frame[self.frame_offset],0,0,0,0,0,0,0,0]
            subval1 = frame[self.frame_offset+1] & 3
            subval2 = frame[self.frame_offset+1] >> 2
            subframe[self.main_subband] = subval1<<2 # ia -> ia00
            subframe[self.main_subband+1] = ((subval2 & 2) << 2) | (subval2 & 1) # ai -> a00i

        else:
            subframe = [frame[self.frame_offset],0,0,0,0,0,0,0,0]

        self.main_subband = subframe[0] & 0x7
        self.inverse = subframe[0] >> 3

        ms = self.subbands[self.main_subband]
        ms.volume = 8

        offset = 1
        for b in range(9):
            cs = self.subbands[b]
            if b < self.main_subband:
                cs.volume = subframe[offset] & 0x7
                cs.inverse = subframe[b] >> 3
                offset += 1
            elif b == self.main_subband:
                cs.inverse = subframe[b] >> 3
            else:
                cs.volume = subframe[offset] >> 1
                cs.inverse = subframe[offset] & 1
                offset += 1

    def generate(self, frame):
        band_frame = array([0.0] * len(frame))
        for i in range(9):
            self.subbands[i].generate(band_frame)
        frame += band_frame * array([meta.main_volumes[15-self.volume]*meta.freq_resp[self.band]/5000.0])

class Frame:
    def __init__(self):
        self.bands = [
                Band(0),
                Band(1),
                Band(2),
                Band(3),
                Band(4),
                Band(5),
                Band(6),
                Band(7),
                Band(8),
                Band(9),
                Band(10),
                Band(11),
                Band(12),
                Band(13),
                Band(14),
                Band(15),
        ] 

    def decode(self, frame):
        volumes = []
        for i in range(16):
            volumes.append([-frame[i],i])
            self.bands[i].format = 1

        volumes.sort()
        sizes = [8,8,8,6,6,2] 
        print volumes

        for v,b in volumes[:6]:
            self.bands[b].format = sizes[0]
            sizes = sizes[1:]
        frame_offset = 16
        for b in range(16):
            self.bands[b].frame_offset = frame_offset
            frame_offset += self.bands[b].format

        for i in range(16):
            self.bands[i].decode(frame)

    def encode(self):
        frame = [0]*64
        for i in range(16):
            self.bands[i].encode(frame)

        return frame

    def __str__(self):
        s = ["Frame([\n"]
        for i in range(16):
            s.append("\t" + str(self.bands[i]).replace("\n","\n\t"))
            s.append("\n")
        s.append("])")
        return "".join(s)

    def generate(self, frame_len = meta.frame_len):
        frame = array([0.0] * frame_len)
        for band in self.bands:
            band.generate(frame)
        frame *= array([5000.0*2.1])
        return frame

    def unpack(self, data):
        data = struct.unpack("B"*32, data)
        fdata = []
        for b in data:
            fdata.append(b & 0xf)
            fdata.append((b>>4)&0xf)

        return fdata

    def pack(self, data = None):
        if data == None:
            data = self.encode()

        ndata = []
        for i in range(32):
            val = data[i*2]|(data[i*2+1]<<4)
            ndata.append(val)

        ndata = struct.pack("B"*32, *ndata)

        return ndata

def decode(fn, ofn, start, num):

    input = open(fn, "rb")
    out = wave.open(ofn, "w")
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(int(meta.frame_len*62.5))
    out.setcomptype("NONE","not compressed")

    print "main_volumes_table", meta.main_volumes
    print "local_volumes_table", meta.local_volumes

    hdr = input.read(2)
    print "hdr", `hdr`

    if start:
        input.read(32*start)

    frame_num = start

    prev_result = array([0.0] * meta.frame_len)

    while 1:
        data = input.read(32)
        if len(data) != 32:
            print "foot", `data`
            break

        frame = Frame()
        fdata = frame.unpack(data)
        frame.decode(fdata)
        if 0:
            edata = frame.encode()
            assert fdata == edata
            edata2 = frame.pack(edata)
            assert data == edata2

        print frame_num, frame
        result = frame.generate().tolist()
        print max(result), min(result)

        out_frame = result * meta.filter1 + prev_result * meta.filter2
        out_frame = [ int(a*0.5) for a in out_frame ]
        odata = struct.pack('h'*meta.frame_len,*out_frame)
        out.writeframes(odata)
        prev_result = result

        frame_num += 1
        if num:
            num -= 1
            if num == 0:
                break

    out.close()

if __name__ == "__main__":
    print sys.argv
    num = None
    start = 0
    if len(sys.argv)>3:
        num = int(sys.argv[3])

    if len(sys.argv)>4:
        start = int(sys.argv[4])

    decode(sys.argv[1], sys.argv[2], start, num)
