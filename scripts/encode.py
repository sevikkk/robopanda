#!/usr/local/bin/python

"""
 sox -V 02\ -\ Winnie-the-Pooh\ -\ Introduction.mp3 -c 1 -s -w test_encode_input.wav trim 0 60 stat
"""

import FFT
import struct
import sys
import wave
import math

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
    print "using %d samples per frame" % frame_len

    out = open(ofn, "w")
    out.write("\x07\x80")
    frame_num = 0
    freq_resp = {
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
    for i in range(16):
        freq_resp[i] = 5000.0/freq_resp[i]

    freq_map = {
             62.5:     62.5,
            125.0:    125.0,
            187.5:    187.5,
            250.0:    250.0,
            312.5:    312.5,
            375.0:    375.0,
            437.5:    437.5,
            500.0:    500.0,
            562.5:    562.5,
            625.0:    625.0,
            687.5:    687.5,
            750.0:    750.0,
            812.5:    812.5,
            875.0:    875.0,
            937.5:    937.5,
           1000.0:   1000.0,
           1062.5:   1062.5,
           1125.0:   1125.0,
           1187.5:   1187.5,
           1250.0:   1250.0,
           1312.5:   1250.0,
           1375.0:   1437.5,
           1437.5:   1437.5,
           1500.0:   1500.0,
           1562.5:   1500.0,
           1625.0:   1500.0,
           1687.5:   1750.0,
           1750.0:   1750.0,
           1812.5:   1750.0,
           1875.0:   2000.0,
           1937.5:   2000.0,
           2000.0:   2000.0,
           2062.5:   2000.0,
           2125.0:   2250.0,
           2187.5:   2250.0,
           2250.0:   2250.0,
           2312.5:   2250.0,
           2375.0:   2500.0,
           2437.5:   2500.0,
           2500.0:   2500.0,
           2562.5:   2500.0,
           2625.0:   2750.0,
           2687.5:   2750.0,
           2750.0:   2750.0,
           2812.5:   2750.0,
           2875.0:   3000.0,
           2937.5:   3000.0,
           3000.0:   3000.0,
           3062.5:   3000.0,
           3125.0:   3250.0,
           3187.5:   3250.0,
           3250.0:   3250.0,
           3312.5:   3250.0,
           3375.0:   3500.0,
           3437.5:   3500.0,
           3500.0:   3500.0,
           3562.5:   3500.0,
           3625.0:   3750.0,
           3687.5:   3750.0,
           3750.0:   3750.0,
           3812.5:   3750.0,
           3875.0:   4000.0,
           3937.5:   4000.0,
           4000.0:   4000.0,
    }

    main_volumes = []
    k = 1
    for i in range(15):
        k = k * 0.6
        main_volumes.append(k)
        
    local_volumes = []
    k = 0.75
    for i in range(7):
        local_volumes.append(k)
        if i<4:
            k = k * 0.75
        else:
            k = k * 0.6

    print "main_volumes_table", main_volumes
    print "local_volumes_table", local_volumes
    window = []
    for i in range(frame_len):
        x = math.pi*(i-frame_len/2)/frame_len*2
        if x == 0:
            win = 1
        else:
            win = math.sin(x)/x
        window.append(win)
    print "window", window

    data = rdata.readframes(frame_len)
    prev_data = struct.unpack("h"*frame_len, data)
    super_max = 0
    while 1:
        cur_data = rdata.readframes(frame_len)

        if len(cur_data) != frame_len*2:
            break

        cur_data = struct.unpack("h"*frame_len, cur_data)

        prev_data = cur_data
        data = list(cur_data)

        for i in range(frame_len):
            data[i] = data[i] * window[i]


        fd = FFT.real_fft(data, frame_len).tolist()
        f = 62.5

        freqs = []
        freqs_data = {}
        freqs_cnt = {}
        for a in fd[1:]:
            p = abs(a)
            g = math.atan2(a.imag,a.real)/math.pi*180

            freqs.append([f,p,g,a])
            mfreq = freq_map[f]

            if not mfreq in freqs_data:
                freqs_data[mfreq] = 0
                freqs_cnt[mfreq] = 0

            freqs_data[mfreq] += abs(a)
            freqs_cnt[mfreq] += 1

            if f >= 4000:
                break

            f += 62.5

        for f in freqs_data.keys():
            freqs_data[f] = freqs_data[f]/freqs_cnt[f]

        if 1:
            freqs.sort(lambda x,y: cmp(y[1],x[1]))
            max_val = freqs[0][1]
            super_max = max(super_max, max_val)

            if max_val>100000:
                limit = max(10000, max_val / 100)
            else:
                limit = 100000000

            print "%6d (%d): "% (frame_num, max_val),
            for f,p,g,a in freqs:
                if p>limit:
                    print "%8.3f: %7d %4d"% (f,p,g),

            print

        k0 = 5000000

        frame = [0] * 64

        for band in (15,14,13,12,11,10,9,8,7,6):
            sb = []

            val = freqs_data.get(band*250,0)
            val = abs(val)/k0 * freq_resp[band]
            sb.append(val)

            volume = 15
            for k in main_volumes:
                if val>k:
                    break
                volume -= 1

            print "band", band, "val", val, "main volume", volume

            frame[band] = volume
            offset = 54 + (band-6)
            frame[offset] = 0 # ignore overlapping subbands

        for band in (5,):
            sb = []
            for sband in (0,3): # 1250 and 1437.5
                val = freqs_data.get(band*250 + sband*62.5,0)
                val = abs(val)/k0 * freq_resp[band]
                sb.append(val)

            if sb[0] < sb[1]: # subband value more than main tone
                if 0:
                    print "WARN: band", band, "main tone volume less than subband, remix"
                    sum = (sb[0] + sb[1])/2/1.75
                    sb[0] = sum
                    sb[1] = sum * 0.75
                else:
                    print "WARN: band", band, "main tone volume less than subband, swap"
                    sb[0], sb[1] = sb[1], sb[0]

            main_volume = 15
            main_volume_k = 1

            for k in main_volumes:
                main_volume_k = k
                if sb[0]>k:
                    break
                main_volume -= 1

            print "band", band, "sb[0]", sb[0], "main volume", main_volume

            sub_volume = 7
            for k in local_volumes:
                if sb[1] > k * main_volume_k:
                    break
                else:
                    sub_volume -= 1
            print "subband", 1, "val", val, "volume", sub_volume

            frame[band] = main_volume
            offset = 52
            frame[offset] = sub_volume << 1 # ignoring phase
            frame[offset+1] = 0 # ignoring overlapping subband

        for band in (4, 3):
            sb = []
            max_val = 0
            max_sub = 0
            for sband in range(4):
                val = freqs_data.get(band*250 + sband*62.5,0)
                val = abs(val)/k0 * freq_resp[band]
                sb.append(val)
                if val>max_val:
                    max_val = val
                    max_sub = sband

            if sb[0] < max_val: # subband value more than main tone
                print "band", band, "WARN: main tone volume less than subband, swap", sb
                sb[0], sb[max_sub] = sb[max_sub], sb[0]

            main_volume = 15
            main_volume_k = 1

            for k in main_volumes:
                main_volume_k = k
                if sb[0]>k:
                    break
                main_volume -= 1

            print "band", band, "sb[0]", sb[0], "main volume", main_volume

            frame[band] = main_volume
            offset = 40 + (band-3) * 6

            for sub in (1,2,3):

                sub_volume = 7
                for k in local_volumes:
                    if sb[sub] > k * main_volume_k:
                        break
                    else:
                        sub_volume -= 1
                print "subband", sub, "val", sb[sub], "volume", sub_volume
                frame[offset+[0,0,1,3][sub]] = sub_volume << 1 # ignoring phase

        prev_band_main_left = 0

        for band in (2, 1, 0):
            sb = []
            max_val = 0
            max_sub = 0

            subs = 4
            if prev_band_main_left:
                subs = 5
                prev_band_main_left = 0

            for sub in range(subs):
                val = freqs_data.get(band*250 + sub*62.5,0)
                val = abs(val)/k0 * freq_resp[band]
                sb.append(val)

                if val>max_val:
                    max_val = val
                    max_sub = sub

            main_volume = 15
            main_volume_k = 1
            for k in main_volumes:
                main_volume_k = k
                if max_val>k:
                    break
                main_volume -= 1

            print "band", band, "max_val", max_val, "main volume", main_volume

            main_offset = [0,1,3,5,7][max_sub]

            frame[band] = main_volume
            offset = 16 + band*8
            frame[offset] = main_offset

            for sub in range(subs):
                val = sb[sub]
                if sub == max_sub:
                    sub_volume = 0
                    print "subband", sub, "is main, skip"
                elif sub == 0:
                    print "subband", sub, "is base but not main, skip to next band"
                    prev_band_main_left = 1
                    sub_volume = 0
                else:
                    sub_volume = 7
                    for k in local_volumes:
                        if val > k * main_volume_k:
                            break
                        else:
                            sub_volume -= 1
                    print "subband", sub, "val", val, "volume", sub_volume
                
                sub_offset = [1,1,3,5,7][sub] # first 1 - for not overwriting main_offset

                frame[offset+sub_offset] = sub_volume << 1

        print frame

        fdata = ""
        for i in range(32):
            val = chr(frame[i*2]|(frame[i*2+1]<<4))
            fdata += val
        out.write(fdata)

        frame_num += 1
    out.write("\xFF\xFF\x00\x00")
    print "super_max:", super_max

if __name__ == "__main__":
    encode(sys.argv[1],sys.argv[2])
