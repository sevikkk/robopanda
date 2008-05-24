#!/usr/local/bin/python

import FFT
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

        fd = FFT.real_fft(data, frame_len).tolist()
        f = 62.5
        print "%6d: "% (frame_num,),
        power_500 = 0
        phase_500 = None
        for a in fd[1:]:
            p = abs(a)
            g = math.atan2(a.real,a.imag)/math.pi*180
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
            shift = (-90 - phase_500)/360*96
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


def analyze(fn, corr = 0.8, shift = 4, frames = None, resync = None):

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
        last_frame = frames[-1]
    else:
        last_frame = -1

    frame_len = 768
    corr_sum = 0
    rdata.readframes(shift)
    last_resync = 0
    
    frame_num = 0

    while 1:
        if corr_sum > 1:
            ns = int(corr_sum)
            corr_sum -= ns
            rdata.readframes(ns)
            data = rdata.readframes(frame_len)
            #print "shifted %d samples forward" % ns
        elif corr_sum < -1:
            ns = int(-corr_sum)
            corr_sum += ns
            data = data[-ns:] + rdata.readframes(frame_len - ns)
            #print "shifted %d samples backward" % ns
        else:
            data = rdata.readframes(frame_len)

        if len(data) != frame_len*2:
            break

        if frame_num == last_frame:
            break

        data = struct.unpack("h"*frame_len, data)

        fd = FFT.real_fft(data, frame_len).tolist()
        f = 62.5
        if (not frames) or (frame_num in frames):
            print "%6d: "% (frame_num,),
            power_500 = 0
            phase_500 = None
            for a in fd[1:]:
                p = abs(a)
                g = math.atan2(a.real,a.imag)/math.pi*180
                if p>100000:
                    print "%8.3f: %7d %4d"% (f,p,g),

                if f == 500:
                    power_500 = p
                    phase_500 = g

                f += 62.5
                if f >= 4000:
                    break
            print

        corr_sum += corr

        if resync and frame_num in resync:
            if power_500>1000000:
                ns = (-90 - phase_500)/360*96
                print "need_resync", -ns, "instead of", corr_sum, "error", (corr_sum + ns)/(frame_num - last_resync)
                last_resync = frame_num
                corr_sum = -ns

        frame_num += 1


if __name__ == "__main__":
    shift = 677
    corr = 0.931128818452
    if 0:
        tune(sys.argv[1], 18, 41, shift, corr)
    if 1:
        analyze(sys.argv[1], shift = shift, corr = corr, 
                resync = [16 + n*31 for n in range(200)])
    if 0:
        for shift2 in range(10):
            print "shift", shift + shift2*96
            analyze(sys.argv[1], shift = shift+shift2*96, corr = corr, frames = [27,49,60,70,82])

    

