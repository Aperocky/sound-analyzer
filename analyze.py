#!/usr/bin/env python3
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import graph_functions as gf
import audio_algorithms as aa
from matplotlib import pyplot as plt

# Peak calculation algorithm used to map frequency array in to 'Peakiness' array.
def peak_calcc(psdarray, index):
    # print(index)
    irange = 4 + int(index/50)
    maxi = max(psdarray[index-irange:index+irange])
    minleft = np.amin(psdarray[index-irange:index])
    minright = np.amin(psdarray[index:index+irange])
    mincons = max(minleft, minright)
    return psdarray[index]**2/mincons/maxi

def peak_calc(psdarray, index):
    # print(index)
    irange = 4
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
        if peaklist[i] > 1 and peaklist[i] > peaklist[i-1] and peaklist[i] > peaklist[i+1]:
            peaks.append(i)
    peaks = np.asarray(peaks)
    return peaks

# Superimpose peak_calc onto analysis
def peak_impose(ax, frequency, peaklist):
    x = list(range(len(peaklist)))
    ax2 = ax.twinx()
    gf.std_graph(ax2, frequency[x], peaklist, c = 'b')
    peaksdex = peak_assign(peaklist)
    gf.button_grapher(ax2, f, peaksdex, peaklist)

if __name__ == '__main__':
    filename = sys.argv[1]
    audio = aa.load_npy(filename)
    # audio -= np.mean(audio)
    f, psd = aa.spectrum(audio)
    ax = gf.init_image()
    gf.semi_graph(ax, f, psd, label = filename)
    maxdex = aa.max_range(psd, 20)
    # gf.button_grapher(ax, f, maxdex, psd)
    peaklist = peak_map(psd)
    peak_impose(ax, f, peaklist)
    plt.show()
