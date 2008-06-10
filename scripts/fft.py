#!/usr/local/bin/python

from numpy.fft import rfft
import struct
import sys
import wave
import math

def tune(fn, start, end, shift = 0, corr = 0):

    rdata = wave.open(fn,'r')
    #print "channels",rdata.getnchannels()
    #print "samplewidth",rdata.getsampwidth()
    #print "framerate",rdata.getframerate()
    #print "comptype",rdata.getcomptype()
    assert rdata.getnchannels() == 1
    assert rdata.getsampwidth() == 2
    assert rdata.getframerate() == 48000
    assert rdata.getcomptype() == "NONE"

    frame_len = 768
    frame_num = 0

    corr_sum =  0

    rdata.readframes(shift)

    shifts = []

    ok = 1
    while 1:
        if corr_sum > 1:
            ns = int(corr_sum)
            corr_sum -= ns
            rdata.readframes(ns)
            data = rdata.readframes(frame_len)
            print "shifted %d samples forward" % ns
        elif corr_sum < -1:
            ns = int(-corr_sum)
            corr_sum += ns
            data = data[-ns:] + rdata.readframes(frame_len - ns)
            print "shifted %d samples backward" % ns
        else:
            data = rdata.readframes(frame_len)

        if len(data) != frame_len*2:
            break

        corr_sum += corr

        if frame_num < start:
            frame_num += 1
            continue

        if frame_num >= end:
            break

        data = struct.unpack("h"*frame_len, data)
        data = [ -a for a in data ]

        fd = rfft(data, frame_len).tolist()
        f = 62.5
        print "%6d: "% (frame_num,),
        power_500 = 0
        phase_500 = None
        for a in fd[1:]:
            p = abs(a)
            g = math.atan2(a.imag,a.real)/math.pi*180
            if p>100000:
                print "%8.3f: %7d %4d"% (f,p,g),
            if f == 500:
                power_500 = p
                phase_500 = g
            f += 62.5
            if f >= 4000:
                break
        print
        if power_500>1000000:
            shift = phase_500/360*96
            print "shift", shift
            shifts.append(shift)
        else:
            ok = 0

        frame_num += 1

    if ok:
        sum = 0 
        num = 0
        pshift = shifts[0]
        for shift in shifts[1:]:
            sum += shift - pshift
            num += 1
            print shift - pshift
            pshift = shift
        print "avg", sum/num


def analyze(fn, corr = 0.8, shift = 4, frames = None, resync = None, big_resync = None, descr = None):

    if descr:
        descr = open(descr, 'r').readlines()

    rdata = wave.open(fn,'r')
    #print "channels",rdata.getnchannels()
    #print "samplewidth",rdata.getsampwidth()
    #print "framerate",rdata.getframerate()
    #print "comptype",rdata.getcomptype()
    assert rdata.getnchannels() == 1
    assert rdata.getsampwidth() == 2
    assert rdata.getframerate() == 48000
    assert rdata.getcomptype() == "NONE"

    if frames:
        frames.sort()
        last_frame = frames[-1] + 1
    else:
        last_frame = -1

    frame_len = 768
    corr_sum = 0
    rdata.readframes(shift)
    last_resync = 0
    
    frame_num = 0
    descr_num = 0

    phase_corr = {
            562.5:  -3,
            750.0:  -20,
            812.5:  -25,
            875.0:  -30,
            937.5:  -35,
            1000.0: -40,
            1250.0: -60,
            1375.5: -65,
            1375.0: -70,
            1437.5: -75,
            1500.0: -80,
    }

    while 1:
        if corr_sum >= 1:
            ns = int(corr_sum)
            corr_sum -= ns
            rdata.readframes(ns)
            #print "shifted %d samples forward" % ns
        elif corr_sum < -1:
            ns = int(-corr_sum)
            corr_sum += ns
            old_pos = rdata.tell()
            rdata.setpos(rdata.tell()-ns)
            new_pos = rdata.tell()
            #print "shifted %d samples backward (%d -> %d)" % (ns, old_pos, new_pos)

        cur_pos = rdata.tell()
        data = rdata.readframes(frame_len)

        if len(data) != frame_len*2:
            break

        if frame_num == last_frame:
            break

        data = struct.unpack("h"*frame_len, data)
        data = [ -a for a in data ]

        fd = rfft(data, frame_len).tolist()
        f = 62.5
        do_print = 0

        if frame_num>20 and (frame_num % 19) == 6:
            if descr and descr_num < len(descr):
                print descr[descr_num][:-1]
                descr_num += 1

        if (not frames) or (frame_num in frames):
            do_print = 1
            #print "%6d(%.5f): "% (frame_num,cur_pos/48000.0),
            print "%6d: "% (frame_num,),

        power_500 = 0
        phase_500 = None
        for a in fd[1:]:
            p = abs(a)
            g = math.atan2(a.imag,a.real)/math.pi*180
            #pc = phase_corr.get(f,0)
            orig_p = p
            p = int(p/200000 + 0.5)*200000
            orig_g = g
            g = (int((g+360)/45 + 0.5)*45) % 360
            if g>180:
                g -= 360

            if do_print and (p>200000):
                print "%8.3f: %7d %4d"% (f,p,g),

            if f == 500:
                power_500 = orig_p
                phase_500 = orig_g

            f += 62.5
            if f >= 4000:
                break
        if do_print:
            print

        if resync and frame_num in resync:
            if power_500>1000000:
                ns = phase_500/360*96
                if big_resync and frame_num in big_resync:
                    ns += big_resync[frame_num] * 96
                    print "big resync", -ns, "instead of", corr_sum, "frame", frame_num

                    last_resync = frame_num
                    corr_sum = -ns
                else:
                    if abs(ns)<5:
                        #print "resync", -ns, "instead of", corr_sum, "error", (corr_sum + ns)/(frame_num - last_resync), "frame", frame_num
                        corr -= (corr_sum + ns)/(frame_num - last_resync)

                        last_resync = frame_num
                        corr_sum = -ns
                    else:
                        print "resync failed, ns", ns,"too big. frame", frame_num
            else:
                print "resync failed, power_500", power_500,"to small. frame", frame_num

        corr_sum += corr

        frame_num += 1


if __name__ == "__main__":
    shift = 582
    corr = 0.938198046099

    shift = 768*6
    corr = 0
    if 0:
        # find corr and initial value of shift
        tune(sys.argv[1], 8, 12, shift, corr)
    if 0:
        # find corrected value of shift for 562.5Hz align
        for shift2 in range(768):
            print "shift", shift + shift2*96
            analyze(sys.argv[1], shift = shift+shift2*96, corr = corr, frames = [0,1,2,3,4,5,6,7,8,9,10,11])
    if 0:
        # fing final value of shift
        for shift2 in range(-3, 4):
            print "shift", shift + shift2
            analyze(sys.argv[1], shift = shift+shift2, corr = corr, frames = range(9,16))
    if 1:
        #full decode for determining of resync and data frames
        analyze(sys.argv[1], shift = shift, corr = corr,
                resync = [18 + n*19 for n in range(20000)],
                frames = [25 + n*19 for n in range(20000)],
                descr = sys.argv[2])
    if 0:
        #decode only needed frames
        analyze(sys.argv[1], shift = shift, corr = corr, 
                resync = [13 + n*31 for n in range(20000)] + [4633],
                frames = [25 + n*31 for n in range(20000)],
                big_resync = {
                    1036: 1, 
                    1253: 4, 
                    4632: 5+16, 4633: 0,
                    4663: 1,
                    4756: 4,
                },
                descr = sys.argv[2])

    

