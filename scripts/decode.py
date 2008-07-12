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
            print "WARNING: clipping %d to 16000" % val
            val = 16000
            self.clips += 1

        if val<-16000:
            print "WARNING: clipping -%d to -16000" % val
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
                (0,  90), #0    500.0
                (1,   0), #1    562.5
                (1,  90), #2    562.5
                (2,   0), #3    625.0
                (2,  90), #4    625.0
                (3,   0), #5    687.5
                (3,  90), #6    687.5
                (4,   0), #7    750.0
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

        # building base frame
        subframe = [0] * 8

        for b in range(1,8):
            pb = self.subbands[b-1]
            cb = self.subbands[b]
            if b <= self.main_subband:
                subframe[b] = pb.volume | (cb.inverse << 3)
            else:
                subframe[b] = (cb.volume<<1) | cb.inverse

        # format metadata
        to_del = 0
        if self.format == 8:
            packed_from = 8
            to_pack = 0
        elif self.format == 6:
            packed_from = 4
            to_pack = 2
        elif self.format == 4:
            packed_from = 1
            to_pack = 3
            if self.main_subband>3:
                to_del = 1
        elif self.format == 2:
            packed_from = 1
            to_pack = 1
            if self.main_subband<1:
                to_del = 0
            elif self.main_subband<7:
                to_del = self.main_subband - 1
            else:
                to_del = 5
        elif self.format == 1:
            packed_from = 1
            to_pack = 0
            to_del = self.main_subband

        # convert packed subbands
        for b in range(packed_from,8):
            if b <= self.main_subband:
                subframe[b] = subframe[b]>>2 # ia00 -> ia
            else:
                subframe[b] = ((subframe[b] & 8) >> 2) | (subframe[b] & 1) # a00i -> ai

        # save saved I
        self.inverse = self.subbands[to_del].inverse

        # delete deleted subbands
        for i in range(to_del):
            del subframe[1]

        # pack packed subbands
        src = packed_from
        dst = packed_from
        for i in range(to_pack):
            subframe[dst] = (subframe[src+1] << 2) | subframe[src]
            src += 2
            dst += 1

        # set main subband and inverse
        subframe[0] = (self.inverse << 3) | self.main_subband

        # put subframe into main frame
        for i in range(self.format):
            frame[self.frame_offset + i] = subframe[i]

    def decode(self, frame):
        # main volume, subband and inverse
        self.volume = frame[self.band]
        self.main_subband = frame[self.frame_offset] & 0x7
        self.inverse = frame[self.frame_offset] >> 3

        # reset subbands
        for b in range(8):
            cs = self.subbands[b]
            cs.volume = 0
            cs.inverse = 0

        #main subband volume
        ms = self.subbands[self.main_subband]
        ms.volume = 8

        # format metadata
        to_del = 0
        if self.format == 8:
            packed_from = 8
            to_pack = 0
        elif self.format == 6:
            packed_from = 4
            to_pack = 2
        elif self.format == 4:
            packed_from = 1
            to_pack = 3
            if self.main_subband>3:
                to_del = 1
        elif self.format == 2:
            packed_from = 1
            to_pack = 1
            if self.main_subband<1:
                to_del = 0
            elif self.main_subband<7:
                to_del = self.main_subband - 1
            else:
                to_del = 5
        elif self.format == 1:
            packed_from = 1
            to_pack = 0
            to_del = self.main_subband

        # unpack packed subbands
        subframe_packed = frame[self.frame_offset:self.frame_offset+self.format]
        subframe = subframe_packed[:] + [0] * (8 - len(subframe_packed))

        src = packed_from
        dst = packed_from
        for i in range(to_pack):
            subframe[dst] = subframe_packed[src] & 3
            subframe[dst+1] = subframe_packed[src]>>2
            src += 1
            dst += 2

        # recover deleted subbands
        for i in range(to_del):
            subframe.insert(1,0)

        subframe = subframe[:8]

        # convert packed subbands
        for b in range(packed_from,8):
            if b <= self.main_subband:
                subframe[b] = subframe[b]<<2 # ia -> ia00
            else:
                subframe[b] = ((subframe[b] & 2) << 2) | (subframe[b] & 1) # ai -> a00i

        # parse base frame
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

        # recover saved I
        self.subbands[to_del].inverse = self.inverse

    def generate(self, frame):
        band_frame = array([0.0] * len(frame))
        for i in range(8):
            self.subbands[i].generate(band_frame)
        frame += band_frame * array([meta.main_volumes[15-self.volume]])

class Frame:
    sizes = [8,8,8,6,6,2] 
    frame_len = 64

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
        sizes = self.sizes[:]
        #print volumes

        for v,b in volumes[:len(sizes)]:
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
        frame = [0]*self.frame_len

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
        data = struct.unpack("B"*(self.frame_len/2), data)
        fdata = []
        for b in data:
            fdata.append(b & 0xf)
            fdata.append((b>>4)&0xf)

        return fdata

    def pack(self, data = None):
        if data == None:
            data = self.encode()

        ndata = []
        nb = len(data)/2
        for i in range(nb):
            val = data[i*2]|(data[i*2+1]<<4)
            ndata.append(val)

        ndata = struct.pack("B"*nb, *ndata)

        return ndata

class Frame7(Frame):
    pass

class Frame9(Frame):
    sizes = [8,8,8,8,8,8,6,6,4,4,2,2,2,2,2,2] 
    frame_len = 96

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
    if hdr[0] == '\x07':
        frame_factory = Frame7
        print "codec 7"
    else:
        frame_factory = Frame9
        print "codec 9"
    #print "hdr", `hdr`

    nb = frame_factory().frame_len/2
    if start:
        input.read(start*nb)

    frame_num = start

    prev_result = array([0.0] * meta.frame_len)
    prev_frame = Frame()
    filter = Filter()

    while 1:
        data = input.read(nb)
        if len(data) != nb:
            #print "foot", `data`
            break

        frame = frame_factory()
        fdata = frame.unpack(data)
        frame.decode(fdata)
        if 1:
            edata = frame.encode()
            if fdata != edata:
                print "fdata", fdata
                print "edata", edata
                ef = frame_factory()
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
