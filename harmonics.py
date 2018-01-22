#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import graph_functions as gf
import audio_algorithms as aa
from itertools import chain

# Find the nearest frequency's index in the array
def find_nearest(frequency, values):
    index = 0
    indexes = []
    diffsave = []
    for i in range(len(frequency)):
        diff = np.abs(frequency[i] - values[index])
        diffsave.append(diff)
        if len(diffsave) < 2:
            continue
        if diffsave[-2] == min(diffsave):
            indexes.append(i-1)
            index += 1
            if index == len(values):
                break
            diffsave = list()
    return indexes

# Peak_calculation.
def peak_calc(psdarray, index):
    # print(index)
    irange = 4 + int(index/50)
    left_bound = index-irange
    right_bound = index+irange
    maxi = max(psdarray[index-irange:index+irange])
    minleft = np.amin(psdarray[index-irange:index])
    while psdarray[left_bound] <= minleft:
        minleft = psdarray[left_bound]
        if left_bound < 4:
            break
        left_bound -= 1
    minright = np.amin(psdarray[index:index+irange])
    while psdarray[right_bound] <= minright:
        minright = psdarray[right_bound]
        right_bound += 1
    mincons = max(minleft, minright)
    return psdarray[index]**2/mincons/maxi

# Map
def peak_map(psdarray):
    peaklist = np.zeros(5)
    for i in range(5,len(psdarray)-50):
        peaklist = np.append(peaklist,peak_calc(psdarray, i))
    padding = np.zeros(50)
    peaklist = np.append(peaklist, padding)
    return peaklist

# Identify the peaks of the peaklist ..
def peak_assign(peaklist):
    peaks = []
    for i in range(len(peaklist)):
        if i < 5:
            continue
        if i > len(peaklist) - 5:
            break
        if peaklist[i] > 0.8 and peaklist[i] > peaklist[i-1] and peaklist[i] > peaklist[i+1]:
            peaks.append(i)
    peaks = np.asarray(peaks)
    return peaks

# Complete the guess work and return an array of frequency checked.
def guesswork(frequency, psdarray, peaklist, peaksdex):
    guess = np.arange(130, 170, 0.25)
    output = []
    for each in guess:
        loudness = 0
        hits = 0
        hitsloc = []
        harmonics = each * np.arange(2,15)
        hardex = find_nearest(frequency, harmonics)
        for i in hardex:
            loudness += peaklist[i]*(10)
            if i in peaksdex:
                hitsloc.append(i)
                hits += 1
        output.append([loudness, hits])
    output = [list(a) for a in zip(guess, output)]
    for i in range(len(output)):
        each = output[i]
        nlist = []
        nlist.append(each[0])
        nlist.extend(each[1])
        output[i] = nlist
    output = np.array(output)
    return output

def run(audio):
    f, psd = aa.spectrum(audio)
    peaklist = peak_map(psd)
    peaksdex = peak_assign(peaklist)
    output = guesswork(f, psd, peaklist, peaksdex)
    return output

if __name__ == '__main__':
    filename = sys.argv[1]
    parts = 1
    if len(sys.argv) > 2:
        parts = int(sys.argv[2])
    au = aa.load_npy(filename)
    # Get the shorter audio pack
    audiolist = np.array_split(au, parts)
    for audio in audiolist:
        output = run(audio)
        # for each in output:
        #     print(each)
        ax = gf.init_image(ylabel = 'POWER')
        gf.std_graph(ax, output[:, 0], output[:, 1])
        ax2 = gf.get_twinx(ax)
        gf.std_graph(ax2, output[:, 0], output[:, 2], c='r')
        plt.show()
