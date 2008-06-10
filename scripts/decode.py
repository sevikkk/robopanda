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
            w = float(i)/frame_len
            self.filter1[i] = w
            self.filter2[frame_len-i-1] = w

meta = Meta(768)

class SubBand:
    def __init__(self, freq, phase):
        self.freq = freq
        self.phase = phase

        self.volume = 0
        self.inverse = 0

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
    def str_subs(self):
        s = []
        if self.base_subband:
            s.append("\t"+str(self.base_subband)+"\n")
        for i in range(self.num_subs):
            s.append("\t"+str(self.subbands[i])+"\n")
        s.append("]")
        return "".join(s)

    def encode(self, frame):
        frame[self.band] = self.volume
        for i in range(self.num_subs):
            frame[self.frame_offset+i] = self.subbands[i].encode()

    def decode(self, frame):
        self.volume = frame[self.band]
        for i in range(self.num_subs):
            self.subbands[i].decode(frame[self.frame_offset+i])

    def generate(self, frame):
        band_frame = array([0.0] * len(frame))
        for i in range(self.num_subs):
            self.subbands[i].generate(band_frame)
        if self.base_subband:
            self.base_subband.generate(band_frame)
        frame += band_frame * array([meta.main_volumes[15-self.volume]*meta.freq_resp[self.band]/5000.0])

class Band8(Band):
    def __init__(self, band):
        self.band = band
        self.base_freq = band * 250.0
        self.frame_offset = 16 + band * 8
        self.num_subs = 8

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
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = None

        self.volume = 0
        self.main_subband = 0
        self.inverse = 0

    def decode(self, frame):
        self.volume = frame[self.band]
        main_subband = frame[self.frame_offset]
        self.main_subband = main_subband & 0x7
        self.inverse = main_subband >> 3
        for i in range(7):
            self.subbands[i+1].decode(frame[self.frame_offset+i+1])

    def generate(self,frame):
        self.subbands[0].inverse = self.inverse
        save = {}
        for i in range(self.main_subband):
            self.subbands[i].volume = self.subbands[i+1].volume
            self.subbands[i].inverse = self.subbands[i+1].inverse
            save[i+1] = (self.subbands[i+1].volume, self.subbands[i+1].inverse)

        self.subbands[self.main_subband].volume = 8
        self.subbands[self.main_subband].inverse = self.inverse

        Band.generate(self, frame)

        for i in range(self.main_subband):
            self.subbands[i+1].volume = save[i+1][0]
            self.subbands[i+1].inverse = save[i+1][1]

        self.subbands[0].volume = 0
        self.subbands[0].inverse = 0

    def encode(self, frame):
        frame[self.band] = self.volume
        frame[self.frame_offset] = self.main_subband | (self.inverse << 3)
        for i in range(7):
            frame[self.frame_offset+i+1] = self.subbands[i+1].encode()

    def __str__(self):
        s = ["Band8(band = %d, freq=%.1f, volume=%d, main_sb=%d, inverse=%d, [\n" % 
                (self.band, self.base_freq, self.volume, self.main_subband, self.inverse)]

        s.append(self.str_subs())
        return "".join(s)

class Band6(Band):
    def __init__(self, band):
        self.band = band
        self.base_freq = band * 250.0
        self.frame_offset = 40 + (band-3) * 6
        self.num_subs = 6

        self.subbands = []
        for freq, phase in [
                (1,  90),
                (2, -90),
                (2, 180),
                (3,   0),
                (3, -90),
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = 0

    def __str__(self):
        s = ["Band6(band = %d, freq=%.1f, volume=%d, [\n" % (self.band, self.base_freq, self.volume)]
        s.append(self.str_subs())
        return "".join(s)

class Band2(Band):
    def __init__(self, band):
        self.band = band
        self.base_freq = band * 250.0
        self.frame_offset = 52
        self.num_subs = 2

        self.subbands = []
        for freq, phase in [
                (3,  -90),
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = 0

    def __str__(self):
        s = ["Band2(band = %d, freq=%.1f, volume=%d, [\n" % (self.band, self.base_freq, self.volume)]
        s.append(self.str_subs())
        return "".join(s)

class Band1(Band):
    def __init__(self, band):
        self.band = band
        self.base_freq = band * 250.0
        self.frame_offset = 54 + (band-6)
        self.num_subs = 1

        self.subbands = []
        for freq, phase in [
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = 0

    def __str__(self):
        s = ["Band1(band = %d, freq=%.1f, volume=%d, [\n" % (self.band, self.base_freq, self.volume)]
        s.append(self.str_subs())
        return "".join(s)

class Frame:
    def __init__(self):
        self.bands = [
                Band8(0),
                Band8(1),
                Band8(2),
                Band6(3),
                Band6(4),
                Band2(5),
                Band1(6),
                Band1(7),
                Band1(8),
                Band1(9),
                Band1(10),
                Band1(11),
                Band1(12),
                Band1(13),
                Band1(14),
                Band1(15),
        ] 

    def decode(self, frame):
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

    def generate(self, frame_len = 768):
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
        if 1:
            edata = frame.encode()
            assert fdata == edata
            edata2 = frame.pack(edata)
            assert data == edata2

        print frame_num, frame
        result = frame.generate().tolist()
        print max(result), min(result)

        out_frame = result * meta.filter1 + prev_result * meta.filter2
        out_frame = [ int(a) for a in out_frame ]
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
