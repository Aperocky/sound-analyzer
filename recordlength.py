#!/usr/bin/env python3
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import sounddevice as sd
import numpy as np
import time as tm

#-------------------------------------------------------------------------------
''' This Script is designed to listen to audio files for certain time period '''
#-------------------------------------------------------------------------------

def record(filename, time=10, fs=44100):
    duration = time
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking = False)
    for i in range(time):
        sys.stdout.write('\r%d seconds elapsed' % (i+1))
        sys.stdout.flush()
        tm.sleep(1)
    recording = recording[:, 0]
    np.save(filename, recording)
    return recording

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('not enough arguments')
    filename = sys.argv[1]
    time_length = int(sys.argv[2])
    fs = 44100
    if len(sys.argv) >= 4:
        fs = int(sys.argv[3])
    record = record(filename, time=time_length, fs=fs)
    if len(record) == time_length * fs:
        print('\nRecord successfully saved!')
