#!/usr/local/bin/python

"""
 sox -V 02\ -\ Winnie-the-Pooh\ -\ Introduction.mp3 -c 1 -s -w test_encode_input.wav trim 0 60 stat
"""

from numpy.fft import rfft
import struct
import sys
import wave
import math
import decode

def encode(fn,ofn):

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

    window = []
    for i in range(frame_len):
        x = math.pi*(i-frame_len/2)/frame_len*2
        if x == 0:
            win = 1
        else:
            win = math.sin(x)/x
        window.append(win)
    #print "window", window

    freq_map = {}
    for b in range(16):
        for sb in range(5):
            f = b * 250.0 + 62.5 * sb
            if sb == 0:
                freq_map[f] =  ((b-1,7),(b,0))
            elif sb == 4:
                freq_map[f] =  ((b,sb*2-1),(b+1,0))
            else:
                freq_map[f] =  ((b,sb*2-1),(b,sb*2))

    super_max = 0
    while 1:
        cur_data = rdata.readframes(frame_len)

        if len(cur_data) != frame_len*2:
            break

        cur_data = struct.unpack("h"*frame_len, cur_data)

        frame = decode.Frame9()

        data = list(cur_data)

        #for i in range(frame_len):
        #    data[i] = data[i] * window[i]

        fd = rfft(data, frame_len).tolist()
        f = 62.5

        for a in fd[1:]:

            (bc, sc), (bs, ss) = freq_map[f]

            if bc>=0 and bc<=15:
                frame.bands[bc].subbands[sc].volume = abs(a.real)/5000000.0
                if a.real<0:
                    frame.bands[bc].subbands[sc].inverse = 1
                else:
                    frame.bands[bc].subbands[sc].inverse = 0

            if bs>=0 and bs<=15:
                frame.bands[bs].subbands[ss].volume = abs(a.imag)/5000000.0
                if a.imag<0:
                    frame.bands[bs].subbands[ss].inverse = 1
                else:
                    frame.bands[bs].subbands[ss].inverse = 0

            if f >= 4000:
                break

            f += 62.5

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

        #print frame
        d = frame.encode()
        #print d

        out.write(frame.pack(d))

        frame_num += 1
        #if frame_num > 100:
        #    break
    out.write("\xFF\xFF\x00\x00")
    print "super_max:", super_max

if __name__ == "__main__":
    encode(sys.argv[1],sys.argv[2])
