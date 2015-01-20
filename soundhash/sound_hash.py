#!/usr/bin/python
# -*- coding: UTF-8 -*-

# python sound_hash.py c6951a1048d39d28610d491cb10f2b12d4169c02

import wave, base64, struct, random, sys, os, math;
import subprocess, re



#print each individual sample to console, used for understanding
def print_sound(filename, cap=0):
    wave_read = wave.open(filename, 'rb');
    print "---------------------------------------"
    print filename
    print "getnchannels " + str( wave_read.getnchannels() );
    print "getsampwidth " + str( wave_read.getsampwidth() );
    print "getframerate " + str( wave_read.getframerate() );
    print "getnframes   " + str( wave_read.getnframes() );
    print "getparams    " + str( wave_read.getparams() );
    # (2, 2, 44100, 192386, 'NONE', 'not compressed')
    print "---------------------------------------"

    counter = 0;
    # range is [-128,128]
    for i in wave_read.readframes(wave_read.getnframes()):
        counter += 1
        #print base64.b64encode(i)
        #print int.from_bytes(i, byteorder='big')
        #print str(type(i)) + str(len(i))
        value = int(struct.unpack("<b", i)[0]/3)
        offset = 60
        if value < 0:
            print (" "*(offset+value)  +  u"⬛"*(-value) + u"│")
        elif value > 0:
            print (" "*(offset)  + u"│" +  u"⬛"*(value)) #u2B1B u25A0 ⬛■
        else:
            print (" "*(offset)  + u"│")
        if cap and counter>cap:
            print " "*(offset-1) + "..."
            break;
    wave_read.close()





def sample_herts(time, herts, amplitude):
    return math.sin(time * herts + 500) * amplitude

def sample_noise(amplitude):
    return random.random()*2*amplitude - amplitude


def hexa_range(hex_str, mini, maxi):
    hexa = int(hex_str, 16) + 0.0
    return int(mini + (maxi - mini) * (hexa / 16.0))

def hexa_percent(hex_str):
    return int(hex_str, 16) / 16.0



fps = 44100.0



def generate_segment(noise_output, percent1, percent2, percent3, percent4):

    SAMPLE_LEN = int(fps); # one second seems good to me

    curve_1_herts = 600 + (5000 - 600) * percent1
    curve_2_herts = 400 + (9000 - 400) * percent2
    curve_3_aplit = 1 + (50-1) * percent3
    melody_tone = 880 + 1760 * percent4

    for i in range(0, SAMPLE_LEN):
        time_percent = (i +0.0 )/ SAMPLE_LEN
        time = i/fps
        value = 0

        value += sample_herts( time, curve_1_herts, 10 + 100 * (time_percent-0.5) )
        value += sample_herts( time, curve_2_herts, 50*(0.1 + ( math.modf(time *3)[0])) )
        #value += sample_noise( curve_3_aplit )

        # long during tunes:
        value += sample_herts( time, 880 + (math.ceil(time*6)*456*percent4 %20)/20 * 1760, 90 )

        value = max(-128, min(value, 127))

        packed_value = struct.pack('<b', value)
        noise_output.writeframesraw(packed_value)
        #noise_output.writeframesraw(packed_value) only if 2 chanels







input_hashes = {}
process = subprocess.Popen(['git', "log", "--pretty=format:'%H'"], stdout=subprocess.PIPE)
out, err = process.communicate()
input_hashes = re.findall(r"[0-9a-z]{40}", out)

if len(sys.argv)>=2:
    if sys.argv[1].find('.wav') != -1:
        print_sound(sys.argv[1], 10)
        exit()
    elif sys.argv[1] == "test":
        input_hashes = {}
    else:
        input_hashes = re.findall(r"[0-9a-z]{40}", out)
else:
    print "listen to last commit"
    input_hashes = {input_hashes[0]}



noise_output = wave.open('noise.wav', 'w')
noise_output.setparams((1, 2, fps, 0, 'NONE', 'not compressed'))


if len(input_hashes)>0:
    print input_hashes
    for hash_itt in input_hashes:
        generate_segment(
            noise_output,
            hexa_percent(hash_itt[0]),
            hexa_percent(hash_itt[1]),
            hexa_percent(hash_itt[2]),
            hexa_percent(hash_itt[3])
            )
else:
    print "generate a randome sound te prove something works"
    generate_segment(
        noise_output,
        random.random(),
        random.random(),
        random.random(),
        random.random()
        )

noise_output.close()


os.system("cat noise.wav | aplay") # heerlijk platform afhankelijk
#print_sound('noise.wav', 10)















# Encoding structs to string
# Frmt     C Type          Python type      Standard size     Notes
# x     pad byte           no value
# c     char               string of length 1     1
# b     signed char        integer          1     (3)
# B     unsigned char      integer          1     (3)
# ?     _Bool              bool             1     (1)
# h     short              integer          2     (3)
# H     unsigned short     integer          2     (3)
# i     int                integer          4     (3)
# I     unsigned int       integer          4     (3)
# l     long               integer          4     (3)
# L     unsigned long      integer          4     (3)
# q     long long          integer          8     (2), (3)
# Q     unsigned long long integer          8     (2), (3)
# f     float              float            4     (4)
# d     double             float            8     (4)
# s     char[]             string
# p     char[]             string
# P     void *             integer
