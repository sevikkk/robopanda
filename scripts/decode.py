#!/usr/local/bin/python

"""
 sox -V 02\ -\ Winnie-the-Pooh\ -\ Introduction.mp3 -c 1 -s -w test_encode_input.wav trim 0 60 stat
"""

import FFT
import struct
import sys
import wave
import math
from Numeric import array


class Meta:

    def __init__(self):
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

meta = Meta()
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
        fi = self.phase/180*math.pi
        delta_fi = self.freq*2*math.pi*0.016/len(frame)

        k = meta.local_volumes[8 - self.volume]
        if self.inverse:
            k = -k

        for i in range(len(frame)):
            x = math.sin(fi) * k
            frame[i] += x
            fi += delta_fi

class Band:
    def str_subs(self):
        s = []
        s.append("\t"+str(self.base_subband)+"\n")
        for i in range(self.num_subs):
            s.append("\t"+str(self.subbands[i])+"\n")
        s.append("]")
        return "".join(s)

    def encode(self, frame):
        frame[band] = self.volume
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
                (0,   0),
                (1,   0),
                (1, -90),
                (2, -90),
                (2, 180),
                (3, 180),
                (3,  90),
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = None
        self.main_subband = None
        self.inverse = None

    def decode(self, frame):
        self.volume = frame[self.band]
        main_subband = frame[self.frame_offset]
        self.main_subband = main_subband & 0x7
        self.inverse = main_subband >> 3
        for i in range(7):
            self.subbands[i+1].decode(frame[self.frame_offset+i+1])

        self.base_subband.freq = self.subbands[self.main_subband].freq
        self.base_subband.phase = self.subbands[self.main_subband].phase
        self.base_subband.inverse = self.inverse

    def encode(self, frame):
        frame[band] = self.volume
        frame[self.frame_offset] = self.main_subband | self.inverse <<3
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
                (1, -90),
                (2, -90),
                (2, 180),
                (3, 180),
                (3,  90),
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = None

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
                (3,  90),
                (4,  90),
            ]:
            self.subbands.append(SubBand(self.base_freq + 62.5 * freq, phase))
        self.base_subband = SubBand(self.base_freq, 0)
        self.base_subband.volume=8

        self.volume = None

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

        self.volume = None

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

    def encode(self, frame):
        for i in range(16):
            self.bands[i].encode(frame)

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
        frame *= array([5000.0])
        return frame

def decode(fn, ofn):

    input = open(fn, "r")
    out = open(ofn, "w")

    meta = Meta()

    print "main_volumes_table", meta.main_volumes
    print "local_volumes_table", meta.local_volumes

    hdr = input.read(2)
    print "hdr", `hdr`

    filter1 = array([0.0] * 768)
    filter2 = array([0.0] * 768)
    prev_result = array([0.0] * 768)

    for i in range(768):
        filter1[i] = i/768.0
        filter2[767-i] = i/768.0

    while 1:
        data = input.read(32)
        if len(data) != 32:
            print "foot", `data`
            break

        data = struct.unpack("B"*32, data)
        fdata = []
        for b in data:
            fdata.append(b & 0xf)
            fdata.append((b>>4)&0xf)

        frame = Frame()
        frame.decode(fdata)
        print frame
        result = frame.generate().tolist()
        print max(result), min(result)

        out_frame = result * filter1 + prev_result * filter2
        out_frame = [ int(a) for a in out_frame ]
        odata = struct.pack('h'*768,*out_frame)
        out.write(odata)
        prev_result = result

if __name__ == "__main__":
    decode(sys.argv[1], sys.argv[2])
