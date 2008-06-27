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

        self.main_volumes = []
        k = 1
        for i in range(15):
            self.main_volumes.append(k)
            k = k * 0.6
        self.main_volumes.append(0)
    
        self.local_volumes = [1.0]
        k = 0.75
        for i in range(6):
            self.local_volumes.append(k)
            if i<4:
                k = k * 0.75
            else:
                k = k * 0.6
        self.local_volumes.append(0)

        self.filter1 = array([0.0] * frame_len)
        self.filter2 = array([0.0] * frame_len)
        for i in range(frame_len):
            #w = math.sin(math.pi/2*i/frame_len)
            #w=w*w
            w = 1.0*i/frame_len
            self.filter1[i] = w
            self.filter2[frame_len-1 - i] = w

    def get_main_volume(self, val):
        volume = 15
        for k in self.main_volumes[1:]:
            if val>k:
                break
            volume -= 1

        return volume

    def get_local_volume(self, main_volume, val):
        main_volume_k = self.main_volumes[15-main_volume]
        sub_volume = 7
        for k in self.local_volumes[1:]:
            if val > k * main_volume_k:
                break
            else:
                sub_volume -= 1

        return sub_volume

meta = Meta(512)

class Filter:
    def __init__(self):
        self.history = [0.0] * (meta.frame_len/64)
        self.max = 0
        self.clips = 0

    def next(self, val):
        self.history = self.history[1:] + [val]
        val = sum(self.history)/len(self.history)
        val = int(val)

        if -val>self.max:
            self.max = -val

        if val>self.max:
            self.max = val

        if val>16000:
            print "WARNING: clipping %d to 16000" % self.max
            val = 16000
            self.clips += 1

        if val<-16000:
            print "WARNING: clipping -%d to -16000" % self.max
            val = -16000
            self.clips += 1

        return val

gencache = {}

class SubBand:
    def __init__(self, freq, phase):
        self.freq = freq
        self.phase = phase

        self.volume = 0
        self.inverse = 0

    def __str__(self):
        return "SubBand(freq=%.1f, phase=%d, volume=%d, inverse=%d)" % (
                self.freq, self.phase, self.volume,  self.inverse)

    def generate(self, frame):

        if self.volume == 0:
            return

        k = meta.local_volumes[8 - self.volume]
        if self.inverse:
            k = -k

        k = -k # robopanda output is inverted

        cache_key = (self.phase, self.freq, k)

        if cache_key in gencache:
            frame_data = gencache[cache_key]
        else:
            fi = self.phase*math.pi/180
            delta_fi = self.freq*2*math.pi*0.016/len(frame)

            frame_data = array([0.0] * meta.frame_len)
            for i in range(len(frame)):
                x = math.sin(fi) * k
                frame_data[i] = x
                fi += delta_fi
            gencache[cache_key] = frame_data

        frame += frame_data

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

        for i in range(8):
            #if self.subbands[i].volume > 0:
            #    s.append("\t"+str(self.subbands[i])+"\n")
            s.append("\t"+str(self.subbands[i])+"\n")

        s.append("]")

        return "".join(s)

    def encode(self, frame):
        #main volume
        frame[self.band] = self.volume

        ms = self.subbands[self.main_subband]
        assert ms.volume == 8

        subframe = [0] * 8

        #main inverse
        if self.format in (6,8):
            self.inverse = self.subbands[0].inverse
            for b in range(1,8):
                pb = self.subbands[b-1]
                cb = self.subbands[b]
                if b <= self.main_subband:
                    subframe[b] = pb.volume | (cb.inverse << 3)
                else:
                    subframe[b] = (cb.volume<<1) | cb.inverse

            if self.format == 6:
                for b in range(4,8):
                    if b <= self.main_subband:
                        subframe[b] = subframe[b]>>2 # ia00 -> ia
                    else:
                        subframe[b] = ((subframe[b] & 8) >> 2) | (subframe[b] & 1) # a00i -> ai
                subframe[4] = (subframe[5] << 2) | subframe[4]
                subframe[5] = (subframe[7] << 2) | subframe[6]

        elif self.format == 2:
            if self.main_subband == 0:
                self.inverse = ms.inverse
                b0 = self.subbands[1].inverse
                b1 = self.subbands[1].volume >> 2
                b2 = self.subbands[2].inverse
                b3 = self.subbands[2].volume >> 2
            elif self.main_subband == 7:
                self.inverse = self.subbands[5].inverse
                b0 = self.subbands[5].volume >> 2
                b1 = self.subbands[6].inverse
                b2 = self.subbands[6].volume >> 2
                b3 = self.subbands[7].inverse
            else:
                self.inverse = self.subbands[self.main_subband-1].inverse
                b0 = self.subbands[self.main_subband-1].volume >> 2
                b1 = self.subbands[self.main_subband].inverse
                b2 = self.subbands[self.main_subband+1].inverse
                b3 = self.subbands[self.main_subband+1].volume >> 2
            subframe[1] = b0 | (b1 << 1) | (b2 << 2) | (b3 << 3)
        else:
            self.inverse = ms.inverse 

        subframe[0] = (self.inverse << 3) | self.main_subband

        for i in range(self.format):
            frame[self.frame_offset + i] = subframe[i]

    def decode(self, frame):
        self.volume = frame[self.band]
        self.main_subband = frame[self.frame_offset] & 0x7
        self.inverse = frame[self.frame_offset] >> 3

        for b in range(8):
            cs = self.subbands[b]
            cs.volume = 0
            cs.inverse = 0

        ms = self.subbands[self.main_subband]
        ms.volume = 8
        ms.inverse = self.inverse

        if self.format in (6,8):
            if self.format == 8:
                subframe = frame[self.frame_offset:self.frame_offset+8]
            else:
                subframe_packed = frame[self.frame_offset:self.frame_offset+6]
                subframe = subframe_packed[:4]
                subframe += [subframe_packed[4] & 3,subframe_packed[4]>>2]
                subframe += [subframe_packed[5] & 3,subframe_packed[5]>>2]

                for b in range(4,8):
                    if b <= self.main_subband:
                        subframe[b] = subframe[b]<<2 # ia -> ia00
                    else:
                        subframe[b] = ((subframe[b] & 2) << 2) | (subframe[b] & 1) # ai -> a00i

            offset = 1
            for b in range(8):
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

        elif self.format == 2:
            dat = frame[self.frame_offset+1]
            b3 = (dat & 8)>>3
            b2 = (dat & 4)>>2
            b1 = (dat & 2)>>1
            b0 = dat & 1
            if self.main_subband == 0:
                self.subbands[0].volume = 8
                self.subbands[0].inverse = self.inverse
                self.subbands[1].volume = b1*4
                self.subbands[1].inverse = b0
                self.subbands[2].volume = b3*4
                self.subbands[2].inverse = b2
            elif self.main_subband == 7:
                self.subbands[7].volume = 8
                self.subbands[7].inverse = b3
                self.subbands[5].volume = b0*4
                self.subbands[5].inverse = self.inverse
                self.subbands[6].volume = b2*4
                self.subbands[6].inverse = b1
            else:
                self.subbands[self.main_subband].inverse = b1
                self.subbands[self.main_subband-1].volume = b0*4
                self.subbands[self.main_subband-1].inverse = self.inverse
                self.subbands[self.main_subband+1].volume = b3*4
                self.subbands[self.main_subband+1].inverse = b2

    def generate(self, frame):
        band_frame = array([0.0] * len(frame))
        for i in range(8):
            self.subbands[i].generate(band_frame)
        frame += band_frame * array([meta.main_volumes[15-self.volume]])

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

    def set_format_and_offsets(self, frame):
        volumes = []
        for i in range(16):
            volumes.append([-self.bands[i].volume, i])
            self.bands[i].format = 1

        volumes.sort()
        sizes = [8,8,8,6,6,2] 
        #print volumes

        for v,b in volumes[:6]:
            self.bands[b].format = sizes[0]
            sizes = sizes[1:]

        frame_offset = 16
        for b in range(16):
            self.bands[b].frame_offset = frame_offset
            frame_offset += self.bands[b].format

    def decode(self, frame):
        for i in range(16):
            self.bands[i].volume = frame[i]

        self.set_format_and_offsets(frame)

        for i in range(16):
            self.bands[i].decode(frame)

    def encode(self):
        # assume that for each subband main_subband, volume set correctly
        # and subband volumes scaled accordingly
        #
        # inverse and format will be recalculated
        frame = [0]*64

        self.set_format_and_offsets(frame)
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

    #print "main_volumes_table", meta.main_volumes
    #print "local_volumes_table", meta.local_volumes

    hdr = input.read(2)
    #print "hdr", `hdr`

    if start:
        input.read(32*start)

    frame_num = start

    prev_result = array([0.0] * meta.frame_len)
    prev_frame = Frame()
    filter = Filter()

    while 1:
        data = input.read(32)
        if len(data) != 32:
            #print "foot", `data`
            break

        frame = Frame()
        fdata = frame.unpack(data)
        frame.decode(fdata)
        if 0:
            edata = frame.encode()
            if fdata != edata:
                print "fdata", fdata
                print "edata", edata
                ef = Frame()
                ef.decode(edata)
                for b in range(16):
                    print b
                    print "original", frame.bands[b]
                    print "encoded ", ef.bands[b]
                assert fdata == edata
            edata2 = frame.pack(edata)
            assert data == edata2

        #print frame_num, frame
        result = frame.generate().tolist()
        #print frame_num, max(result), min(result)

        out_frame = result * meta.filter1 + prev_result * meta.filter2
        out_frame = [ int(filter.next(a*4000.0)) for a in out_frame ]
        odata = struct.pack('h'*meta.frame_len,*out_frame)
        out.writeframes(odata)
        prev_result = result

        frame_num += 1
        if num:
            num -= 1
            if num == 0:
                break

    print "max value", filter.max, "clips", filter.clips
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
