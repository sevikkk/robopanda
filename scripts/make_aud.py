#!/usr/local/bin/python

import sys
import random

def pack(data):
    return [int(a,16) for a in data.split()]

def pack2(data):
    return "".join([chr(a) for a in data])

hdr = pack2(pack("07 80"))
foot = pack2(pack("FF FF 00 00"))

out = open("out.aud","wb")

'''
silence = pack("""
00 00 00 00 00 00 00 00 #main band volumes
18 11 11 11             #0 band   0       1 bit something 
                                          3 bits - offset + phase (same as subbands)
                             # subbands
                             #  62.5 sin  4 bits volume
                             #  62.5 cos  4 bits volume
                             # 125.0 sin  4 bits volume
                             # 125.0 cos  4 bits volume
                             # 187.5 sin  4 bits volume
                             # 187.5 cos  4 bits volume
                             # 250.0 sin  4 bits volume

18 11 11 11             #1      250
                             # subbands as in 0 + 250
18 11 11 11             #2      500
                             # subbands as in 0 + 500
18 11 55                #3      750
18 11 55                #4     1000
58                      #5     1250
8                       #6     1500
8                       #7     1750
8                       #8     2000
8                       #9     2250
8                       #10    2500
8                       #11    2750
8                       #12    3000
8                       #13    3250
8                       #14    3500
8                       #15    3750
""")
'''

silence = pack("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
frame1 = pack("71 7B 5B 89 B9 EC DC DB 70 91 CF 68 B8 D8 82 F2 B4 92 32 39 52 0A C1 2E 03 A7 DB 06 42 73 D2 D8")

data = silence*10 + frame1 + silence*10

#test_bits
if 0:
    for i in range(len(silence)):
        for j in range(8):
            test_frame = silence[:]
            mask = 1<<j
            test_frame[i] ^= mask
            data += test_frame * 10

#test_volumes
if 0:
    for i in range(16):  # subband
        for j in range(16): # volumes
            test_frame = silence[:]
            bnum, shift = divmod(i,2)
            shift *= 4
            test_frame[bnum] = j << shift
            data += test_frame * 10

#test_superposition
if 0:
    for i in range(50):  # sample
        test_frame = silence[:]
        for j in random.sample(range(16),5):
            bnum, shift = divmod(j,2)
            shift *= 4
            test_frame[bnum] |= 10 << shift

        data += test_frame * 10

#test_bits_for_band
if 0:
    for i in range(16): # band
        for j in range(8, len(silence)): # remaining bytes
            for k in range(8): # bits
                test_frame = silence[:]

                # set volume for band
                bnum, shift = divmod(i,2)
                shift *= 4
                test_frame[bnum] |= 10 << shift

                # set bits
                mask = 1<<k
                test_frame[j] ^= mask
                data += test_frame * 10


#test_bits_for_all_bands
if 0:
    test_frame_base = silence[:]
    for i in range(16): # band
        # set volume for band
        bnum, shift = divmod(i,2)
        shift *= 4
        test_frame_base[bnum] |= 14 << shift

    for j in range(8, len(silence)): # remaining bytes
        for k in range(8): # bits
            test_frame = test_frame_base[:]

            # set bits
            mask = 1<<k
            test_frame[j] ^= mask
            data += test_frame * 10

#test_bits_for_band2
if 0:
    test_frame_base = silence[:]
    i = 2

    # set volume for band i
    bnum, shift = divmod(i,2)
    shift *= 4
    test_frame_base[bnum] |= 14 << shift

    for j in range(8): # subband
        bnum, shift = divmod(j,2)
        bnum += 16
        shift *= 4
        for k in range(16): # values
            test_frame = test_frame_base[:]

            # set bits
            test_frame[bnum] = k << shift

            data += test_frame_base * 10
            data += test_frame * 10
            data += test_frame_base * 10
            data += silence


#test_bits_for_band3
if 0:
    carrier_frame = silence[:]
    carrier_frame[1] |= 14 # main tone volume 14
    carrier_frame[16] |= 14 << 4 # first subband volume 7, phase 0

    test_frame_base = silence[:]

    i = 3

    # set volume for band i
    bnum, shift = divmod(i,2)
    shift *= 4
    test_frame_base[bnum] |= 14 << shift

    for j in range(6): # subband
        bnum, shift = divmod(j,2)
        bnum += 20
        shift *= 4
        val_range = 16

        for k in range(val_range): # values
            test_frame = test_frame_base[:]

            # set bits
            test_frame[bnum] = k << shift

            data += carrier_frame * 10
            data += test_frame * 10
            data += carrier_frame * 10
            data += silence


#test_bits_for_band5
if 0:
    carrier_frame = silence[:]
    carrier_frame[1] |= 14 # main tone volume 14
    carrier_frame[16] |= 14 << 4 # first subband volume 7, phase 0

    test_frame_base = silence[:]

    i = 5

    # set volume for band i
    bnum, shift = divmod(i,2)
    shift *= 4
    test_frame_base[bnum] |= 14 << shift

    for j in range(2): # subband
        bnum, shift = divmod(j,2)
        bnum += 26
        shift *= 4
        val_range = 16

        for k in range(val_range): # values
            test_frame = test_frame_base[:]

            # set bits
            test_frame[bnum] = k << shift

            data += carrier_frame * 10
            data += test_frame * 10
            data += carrier_frame * 10
            data += silence

#test_bits_for_band6
if 0:
    carrier_frame = silence[:]
    carrier_frame[1] |= 14 # main tone volume 14
    carrier_frame[16] |= 14 << 4 # first subband volume 7, phase 0

    test_frame_base = silence[:]

    i = 6

    # set volume for band i
    bnum, shift = divmod(i,2)
    shift *= 4
    test_frame_base[bnum] |= 14 << shift

    for j in range(1): # subband
        bnum, shift = divmod(j,2)
        bnum += 27
        shift *= 4
        val_range = 16

        for k in range(val_range): # values
            test_frame = test_frame_base[:]

            # set bits
            test_frame[bnum] = k << shift

            data += carrier_frame * 10
            data += test_frame * 10
            data += carrier_frame * 10
            data += silence

#test_all_subbands_freqs
if 0:
    silence = [0] * 64 # nibbles
    carrier_frame = silence[:]
    carrier_frame[2] = 14 # main tone volume 14
    carrier_frame[33] = 14 # first subband volume 7, phase 0

    test_frames = []

    for band in range(16):
        sys.stderr.write("band: %d\n" % band)
        if band<=2:
            first_is_main = 1
            num_subs = 8
            offset = 16 + band * 8
        elif band<=4:
            first_is_main = 0
            num_subs = 6
            offset = 40 + (band-3) * 6
        elif band<=5:
            first_is_main = 0
            num_subs = 2
            offset = 52
        else:
            first_is_main = 0
            num_subs = 1
            offset = 54 + (band-6)

        # check for main volume coefs
        for main_volume in range(1,16):
            test_frame = silence[:] # nibbles
            test_frame[band] = main_volume
            if band == 0:
                test_frame[16] = 3

            test_frames.append(test_frame)
            sys.stderr.write("FRAME: main volume: band %d value %d\n" % (band, main_volume))

        #check subbands
        for subband in range(num_subs):
            sys.stderr.write("subband: %d\n" % subband)
            if first_is_main and (subband == 0):
                #for bands with main tone offsets, check offsets
                for value in range(16):
                    test_frame = silence[:] # nibbles
                    test_frame[band] = 14
                    test_frame[offset + subband] = value

                    sys.stderr.write("FRAME: main offset: band %d offset %d\n" % (band, value))
                    test_frames.append(test_frame)
            elif band == 2 and subband == 6:
                #check main and local volume interaction
                for main_volume in range(16):
                    for local_volume_and_phase in range(16):
                        test_frame = silence[:] # nibbles
                        test_frame[band] = main_volume
                        test_frame[offset + subband] = local_volume_and_phase

                        test_frames.append(test_frame)
                        sys.stderr.write("FRAME: first subband: band %d subband %d main volume %d local volume %d\n" % (band, subband, main_volume, local_volume_and_phase))
                first = 0
            else:
                #for other subbands check freq
                test_frame = silence[:] # nibbles
                test_frame[band] = 14
                test_frame[offset+subband] = 14

                sys.stderr.write("FRAME: subband freq: band %d subband %d\n" % (band, subband))
                test_frames.append(test_frame)

    sys.stderr.write("expand\n")
    mdata = []
    for test_frame in test_frames:
        mdata += carrier_frame * 10
        mdata += test_frame * 10
        mdata += carrier_frame * 10
        mdata += silence

    sys.stderr.write("pack\n")
    ndata = []
    i = 0
    while i < len(mdata):
        val = mdata[i]|(mdata[i+1]<<4)
        try:
            c = chr(val)
        except:
            print "val:", val, "at", i
            raise
        ndata.append(val)
        i += 2

    data += ndata

#test_band8_interactions
if 0:
    from decode import Frame
    
    silence = Frame()

    start_marker = Frame()
    start_marker.bands[10].volume=14

    end_marker = Frame()
    end_marker.bands[8].volume=14

    start_frame = Frame()
    start_frame.bands[2].volume=14
    start_frame.bands[2].subbands[1].volume=7

    end_frame = Frame()
    end_frame.bands[2].volume=14
    end_frame.bands[2].subbands[3].volume=7

    data = silence.pack() * 5 + start_marker.pack()*3 + silence.pack() * 4
    data += start_frame.pack()*5 + silence.pack() * 4

    frame_num = 0
    for main_subband in range(8):
        for main_inverse in [0,1]:
            for subband in range(7):
                for subband_inverse in [0,1]:
                    frame = Frame()
                    frame.bands[1].volume = 14
                    frame.bands[1].main_subband = main_subband
                    frame.bands[1].inverse = main_inverse
                    frame.bands[1].subbands[subband+1].volume = 7
                    frame.bands[1].subbands[subband+1].inverse = subband_inverse
                    frame.bands[2].volume = 14
                    frame.bands[2].main_subband = 3
                    sys.stderr.write("FRAME: %d: main_subband %d main_inverse %d subband %d subband_inverse %d\n" % 
                            (frame_num, main_subband, main_inverse, subband + 1, subband_inverse))
                    frame_num += 1

                    data += start_frame.pack()*5 + frame.pack()*10 + silence.pack()*4
                    #data += frame.pack() * 10

    data += silence.pack() * 4 + end_marker.pack() + silence.pack() * 4

    out.write(hdr)
    out.write(data)
    out.write(foot)
    sys.exit(0)

#test_00837_slow
if 0:
    from decode import Frame

    f = open('dump_cartridge_black/00837.aud', 'rb')
    f.read(2)
    out.write(hdr)

    for i in range(40):
        orig_data = f.read(32)
    
        orig_frame = Frame()
        orig_frame.decode(orig_frame.unpack(orig_data))
        for b in range(16):
            frame = Frame()
            for j in range(b+1):
                frame.bands[j] = orig_frame.bands[j]
            out.write(orig_frame.pack()*10)
            out.write(frame.pack()*10)

    out.write(foot)
    sys.exit(0)
        
#test_band2_interactions
if 1:
    from decode import Frame
    
    silence = Frame()

    start_marker = Frame()
    start_marker.bands[10].volume=14

    end_marker = Frame()
    end_marker.bands[8].volume=14

    start_frame = Frame()
    start_frame.bands[2].volume=14
    start_frame.bands[2].subbands[1].volume=7

    end_frame = Frame()
    end_frame.bands[2].volume=14
    end_frame.bands[2].subbands[3].volume=7

    data = silence.pack() * 15 + start_marker.pack()*3 + silence.pack() * 4
    data += start_frame.pack()*20 + silence.pack() * 4

    frame_num = 0
    for ms in range(16):
      for add_nibble in [0]:
        for add_nibble_val in [0]:
            frame = Frame()
            frame.bands[15].volume = 14    # 8
            frame.bands[14].volume = 13   # 8
            frame.bands[13].volume = 12   # 8
            frame.bands[12].volume = 11    # 6
            frame.bands[11].volume = 10   # 6
            frame.bands[10].volume = 9   # 2
            frame.bands[2].volume = 8    # 1

            f = frame.encode()
            f[18] = ms
            f[add_nibble] = add_nibble_val
            sys.stderr.write("FRAME: %d: ms %d add_nibble %d add_nibble_val %d \n" % 
                    (frame_num, ms, add_nibble, add_nibble_val))
            frame_num += 1

            data += start_frame.pack()*5 + frame.pack(f)*10 + silence.pack()*4

    data += end_marker.pack() + silence.pack() * 4

    out.write(hdr)
    out.write(data)
    out.write(foot)
    sys.exit(0)

silence = pack("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
data += silence*10 + frame1 + silence*10
data = hdr + pack2(data) + foot

out.write(data)
