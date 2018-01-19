#!/usr/bin/env python3
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import sounddevice as sd
import numpy as np
import time as tm

def replay(path, fs=44100):
    sound = np.load(path)
    print(sound)
    sd.play(sound, fs, blocking = True)

if __name__ == '__main__':
    path = sys.argv[1]
    fs = 44100
    if len(sys.argv) > 2:
        fs = int(sys.argv[2])
    replay(path, fs)
