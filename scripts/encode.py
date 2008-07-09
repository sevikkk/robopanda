#!/usr/local/bin/python

"""
 sox -V 02\ -\ Winnie-the-Pooh\ -\ Introduction.mp3 -c 1 -s -w test_encode_input.wav trim 0 60 stat
"""

from numpy.fft import rfft
from numpy import array
import struct
import sys
import wave
import math
import decode

def encode(fn,ofn):

    freq_resp = {
            0:     10000,
            1:     7920,
            2:     4715,
            3:     4469,
            4:     4141,
            5:     3785,
            6:     3416,
            7:     3047,
            8:     2590,
            9:     2360,
            10:    2049,
            11:    1765,
            12:    1503,
            13:    1267,
            14:    1057,
            15:    871,
            16:    871
    }
    rdata = wave.open(fn,'r')
    #print "channels",rdata.getnchannels()
    #print "samplewidth",rdata.getsampwidth()
    #print "framerate",rdata.getframerate()
    #print "comptype",rdata.getcomptype()
    assert rdata.getnchannels() == 1
    assert rdata.getsampwidth() == 2
    assert rdata.getcomptype() == "NONE"

    rate = rdata.getframerate()
    frame_len = int(rate * 0.016)

    decode.meta = decode.Meta(frame_len)

    #print "using %d samples per frame" % frame_len

    out = open(ofn, "wb")
    out.write("\x09\x80")
    frame_num = 0

    freq_map = {}
    for b in range(16):
        for sb in range(5):
            f = b * 250.0 + 62.5 * sb
            if sb == 0:
                freq_map[f] =  ((b,0), (b-1,7))
            elif sb == 4:
                freq_map[f] =  ((b+1,0),(b,sb*2-1))
            else:
                freq_map[f] =  ((b,sb*2),(b,sb*2-1))

    cur_data = rdata.readframes(frame_len)
    cur_data = array(struct.unpack("h"*frame_len, cur_data))
    next_data = rdata.readframes(frame_len)
    next_data = array(struct.unpack("h"*frame_len, next_data))

    super_max = 0
    while 1:
        prev_data = cur_data
        cur_data = next_data
        next_data = rdata.readframes(frame_len)

        if len(next_data) != frame_len*2:
            break

        next_data = array(struct.unpack("h"*frame_len, next_data))

        frame = decode.Frame9()

        #data = cur_data - decode.meta.filter1*(next_data - decode.meta.filter2*cur_data) - decode.meta.filter2*(prev_data - decode.meta.filter2*cur_data)
        data = cur_data + cur_data + next_data + prev_data
        #data = cur_data
        data = data * array([1.0/16384/3])

        fd = rfft(data, frame_len).tolist()
        f = 62.5

        for a in fd[1:]:

            (bc, sc), (bs, ss) = freq_map[f]
            corr = 5000.0/freq_resp[bc]

            if f<250:
                a = abs(a) + 0j

            if bc>=0 and bc<=15:
                frame.bands[bc].subbands[sc].volume = abs(a.real)/decode.meta.frame_len*corr
                if a.real>0:
                    frame.bands[bc].subbands[sc].inverse = 0
                else:
                    frame.bands[bc].subbands[sc].inverse = 1

            if bs>=0 and bs<=15:
                frame.bands[bs].subbands[ss].volume = abs(a.imag)/decode.meta.frame_len*corr
                if a.imag>0:
                    frame.bands[bs].subbands[ss].inverse = 0
                else:
                    frame.bands[bs].subbands[ss].inverse = 1

            if f >= 4000:
                break

            f += 62.5

        if 0:
            s = ["%5d" % frame_num]
            for b in range(3):
                s.append("|")
                s.append("%6.3f" % frame.bands[b].volume)
                for sb in range(8):
                    v = frame.bands[b].subbands[sb].volume
                    if frame.bands[b].subbands[sb].inverse:
                        v = -v
                    s.append("%6.3f" % v)

            print " ".join(s)

        #print frame
        for b in range(16):
            volumes = []
            max_volume = 0
            main_subband = 0
            for sb in range(8):
                sbo = frame.bands[b].subbands[sb]
                if sbo.volume>super_max:
                    super_max = sbo.volume
                if sbo.volume>max_volume:
                    max_volume = sbo.volume
                    main_subband = sb

            main_volume = decode.meta.get_main_volume(max_volume)
            frame.bands[b].volume = main_volume
            frame.bands[b].main_subband = main_subband
            for sb in range(8):
                sbo = frame.bands[b].subbands[sb]
                if sb == main_subband:
                    sbo.volume = 8
                else:
                    sbo.volume = decode.meta.get_local_volume(main_volume, sbo.volume)

        if 0:
            s = ["%5d" % frame_num]
            for b in range(3):
                s.append("|")
                s.append("%6d" % frame.bands[b].volume)
                for sb in range(8):
                    v = frame.bands[b].subbands[sb].volume
                    if frame.bands[b].subbands[sb].inverse:
                        v = -v
                    s.append("%6d" % v)

            print " ".join(s)

        #print frame
        d = frame.encode()
        #print d

        out.write(frame.pack(d))

        frame_num += 1
        #if frame_num > 100:
        #    break
        if 1:
            if frame_num % 20 == 0:
                print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b",frame_num,
                sys.stdout.flush()
    out.write("\xFF\xFF\x00\x00")
    print "super_max:", super_max

if __name__ == "__main__":
    encode(sys.argv[1],sys.argv[2])
