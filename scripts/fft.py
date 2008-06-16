#!/usr/local/bin/python

from numpy.fft import rfft
import struct
import sys
import wave
import math
import Image

class Analyzer:
    def __init__(self, fn):
        rdata = wave.open(fn,'r')
        assert rdata.getnchannels() == 1
        assert rdata.getsampwidth() == 2
        assert rdata.getcomptype() == "NONE"
        assert rdata.getframerate() == 32000

        self.rdata = rdata
        self.frame_len = 512
        self.corr = 0
        self.corr_sum = 0
        self.shift = 0
        self.base = 0
        self.descr = {}
        self.pos = 0

    def read_frame(self, frame_len = None):
        if not frame_len:
            frame_len = self.frame_len

        data = self.rdata.readframes(frame_len)
        data = struct.unpack("h"*frame_len, data)
        data = [ -a for a in data ]

        fd = rfft(data, frame_len).tolist()
        fd = fd[1:]
        return fd

    def read_frame_with_corr(self):
        if self.corr_sum>1:
            ns = int(self.corr_sum)
            self.corr_sum -= ns
        elif self.corr_sum < -1:
            ns = int(self.corr_sum)
            self.corr_sum -= ns
        else:
            ns = 0

        if ns != 0:
            pos = self.rdata.tell() + ns
            self.rdata.setpos(pos)
        else:
            pos = self.rdata.tell()

        self.pos = pos*0.016/self.frame_len

        res = self.read_frame()
        self.corr_sum += self.corr

        return res

    def tune(self):

        #print "channels",rdata.getnchannels()
        #print "samplewidth",rdata.getsampwidth()
        #print "framerate",rdata.getframerate()
        #print "comptype",rdata.getcomptype()

            
        print ">>> search 2000 Hz burst"
        frame_num = 0

        b2000_start = None

        while 1:
            frame_len_2000 = self.frame_len/8
            fd = self.read_frame(frame_len_2000)
            total = 1
            for a in fd:
                total += abs(a)

            p2000 = abs(fd[4])/total
            #print "%3d %10.1f %0.2f" % (frame_num,total,p2000)
            if not b2000_start:
                if p2000>0.5:
                    b2000_start = frame_num
            elif p2000<0.5:
                    b2000_end = frame_num
                    break

            frame_num += 1
            if frame_num == 1000:
                break

        if (not b2000_start) or (not b2000_end) or (b2000_end - b2000_start>32) or (b2000_end - b2000_start<28):
            raise RuntimeError,"valid 2 kHz burst not found"

        print "found:", b2000_start, "-", b2000_end, "len", b2000_end - b2000_start

        self.base = int((b2000_start + b2000_end)/2 * frame_len_2000 + self.frame_len * 7.5)

        #print b500_zone*0.016/self.frame_len
        self.rdata.setpos(self.base)

        print ">>> search 500 Hz burst and tuning per frame correction"
        frame_num = 0

        shifts = []

        ok = 1
        while 1:
            fd = self.read_frame()

            f = 62.5
            #print "%6d: "% (frame_num,),
            power_500 = 0
            phase_500 = None
            for a in fd:
                p = abs(a)
                g = math.atan2(a.imag,a.real)/math.pi*180
                #if p>100000:
                #    print "%8.3f: %7d %4d"% (f,p,g),
                if f == 500:
                    power_500 = p
                    phase_500 = g
                f += 62.5
                if f >= 4000:
                    break
            #print
            if power_500>1000000:
                shift = phase_500/360*(self.frame_len/8)
                #print "shift", shift
                shifts.append(shift)
            else:
                ok = 0

            frame_num += 1
            if frame_num == 15:
                break

        #print ok, shifts
        if not ok:
            raise RuntimeError, "valid 500Hz burst not found"

        psum = 0 
        num = 0
        pshift = shifts[0]
        for shift in shifts[1:]:
            psum += shift - pshift
            num += 1
            #print "corr", shift - pshift
            pshift = shift
        self.corr = -psum/num
        print "per frame correction", self.corr

        print ">>> tune 500Hz and 562.5Hz phase"

        self.rdata.setpos(self.base)
        self.corr_sum = 0
        frame_num = 0
        ok = 1
        shifts = []
        shifts_562 = []

        while 1:
            fd = self.read_frame_with_corr()

            f = 62.5
            print "%6d: "% (frame_num,),
            power_500 = 0
            phase_500 = None
            power_562 = 0
            phase_562 = None
            for a in fd:
                p = abs(a)
                g = math.atan2(a.imag,a.real)/math.pi*180
                if p>100000:
                    print "%8.3f: %7d %4d"% (f,p,g),
                if f == 500:
                    power_500 = p
                    phase_500 = g
                if f == 562.5:
                    power_562 = p
                    phase_562 = g
                f += 62.5
                if f >= 4000:
                    break
            print
            if power_500>500000 and power_562>500000:
                shift_500 = phase_500/360*(self.frame_len/8)
                shift_562 = phase_562/360*(self.frame_len/9)
                print "shift", shift_500, shift_562
                print "pos",self.rdata.tell()*0.016/self.frame_len
                shifts.append(shift_500)
                shifts_562.append(shift_562)
            else:
                ok = 0

            frame_num += 1
            if frame_num == 15:
                break

        #print ok, shifts
        if not ok:
            raise RuntimeError, "valid 500Hz burst not found"

        shift_500 = sum(shifts)/len(shifts)
        shift_562 = sum(shifts_562)/len(shifts_562)

        self.shift = -shift_500
        shift_562 += self.shift

        print shift_562

        if shift_562>6 and shift_562<8:
            n = 3# +90 1
        elif shift_562>13 and shift_562<15:
            n = 2# +90 0
        else:
            n = 0 # 0 - 0
            n = 1 # 0 - 45
            n = 4 # 0 - 45

        n = (self.frame_len/8)*n
        self.shift += n
        print "shift", self.shift

        if 1:
            frame=1
            print ">>> check phase for frame %d" % frame

            self.rdata.setpos(self.base)
            self.corr_sum = self.shift + (23+19*frame)*(self.frame_len+self.corr)
            frame_num = 0

            while 1:
                fd = self.read_frame_with_corr()

                f = 62.5
                print "%6d(%.3f): "% (frame_num, self.pos),
                for a in fd:
                    p = abs(a)
                    g = math.atan2(a.imag,a.real)/math.pi*180
                    if p>100000:
                        print "%8.3f: %7d %4d"% (f,p,g),
                    f += 62.5
                    if f >= 4000:
                        break
                print

                frame_num += 1
                if frame_num == 19:
                    break

    def load_descr(self, descr):
        for l in open(descr,"r").readlines():
            l = l[:-1].split(None,2)
            if len(l)!=3:
                continue
            if l[0] != "FRAME:":
                continue
            sample_num = int(l[1][:-1])
            self.descr[sample_num] = l[2]

    def dump(self):
        start_sample= 0
        self.rdata.setpos(self.base)
        self.corr_sum = self.shift + (19+19*start_sample)*(self.frame_len+self.corr)
        sample_num = 0
        frame_num = 0

        shift_500 = 0

        cur_descr = ""

        while 1:
            if frame_num == 0:
                if sample_num in self.descr:
                    #print "###",self.descr[sample_num]
                    cur_descr = self.descr[sample_num]
                sample_num += 1
                frame_num = 0

            fd = self.read_frame_with_corr()

            p500 = 0
            g500 = 0
            f = 62.5
            
            prn = []

            for a in fd:
                if f<500:
                    f += 62.5
                    continue

                p = abs(a)
                g = math.atan2(a.imag,a.real)/math.pi*180
                if f == 500 and p>100000:
                    p500 = p
                    g500 = g

                if abs(a.imag)>30000:
                    if a.imag<0:
                        k = -1
                    else:
                        k = 1
                    prn.append("%5.0fs: %4d"% (f*k,k*a.imag/10000))
                else:
                    prn.append(" "*12)

                if abs(a.real)>30000:
                    if a.real<0:
                        k = -1
                    else:
                        k = 1
                    prn.append("%5.0fc: %4d"% (k*f,k*a.real/10000))
                else:
                    prn.append(" "*12)

                f += 62.5
                if f > 750:
                    break

            prn.append("%6d(%.3f):"% (frame_num, self.pos))

            if cur_descr:
                prn.append(cur_descr)

            if frame_num in (11,):
                print " ".join(prn)

            if frame_num in (4,5):
                if p500<1000000:
                    raise RuntimeError, "500Hz burst not found"

                shift_500 += g500/360*(self.frame_len/8)
            if frame_num == 5:
                #print "need corr", shift_500/3
                self.corr_sum -= shift_500/2

            frame_num += 1

            if frame_num == 19:
                frame_num = 0
                cur_descr = ""

if __name__ == "__main__":
    analyzer = Analyzer(sys.argv[1])
    analyzer.tune()
    if len(sys.argv)>2:
        analyzer.load_descr(sys.argv[2])
    analyzer.dump()
