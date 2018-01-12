#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import graph_functions as gf
import audio_algorithms as aa

# Find the nearest frequency's index in the array
def find_nearest(frequency, values):
    indexes = np.searchsorted(frequency, values, side="left")
    return indexes

# Peak_calculation.
def peak_calc(psdarray, index):
    # print(index)
    irange = 4 + int(index/20)
    maxi = max(psdarray[index-irange:index+irange])
    minleft = np.amin(psdarray[index-irange:index])
    minright = np.amin(psdarray[index:index+irange])
    mincons = max(minleft, minright)
    return psdarray[index]**2/mincons/maxi

# Complete the guess work and return an array of frequency checked.
def guesswork(frequency, psdarray):
    guess = np.arange(133, 160, 1)
    output = []
    for each in guess:
        harmonics = each * np.arange(2, 20)
        hardex = find_nearest(frequency, harmonics)
        sumpeaks = 0
        for index in hardex:
            sumpeaks += peak_calc(psdarray, index)
        output.append(sumpeaks)
    output = np.asarray(output)
    return guess, output

if __name__ == '__main__':
    filename = sys.argv[1]
    audio = aa.load_npy(filename)
    f, psd = aa.spectrum(audio)
    guess, output = guesswork(f, psd)
    print(guess)
    print(output)
