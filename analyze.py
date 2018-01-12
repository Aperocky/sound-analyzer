#!/usr/bin/env python3
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import graph_functions as gf
import audio_algorithms as aa
from matplotlib import pyplot as plt

# Peak calculation algorithm used to map frequency array in to 'Peakiness' array.
def peak_calc(psdarray, index):
    # print(index)
    irange = 4 + int(index/20)
    maxi = max(psdarray[index-irange:index+irange])
    minleft = np.amin(psdarray[index-irange:index])
    minright = np.amin(psdarray[index:index+irange])
    mincons = max(minleft, minright)
    return psdarray[index]**2/mincons/maxi

def peak_map(psdarray):
    peaklist = np.zeros(5)
    for i in range(5,len(psdarray)-50):
        peaklist = np.append(peaklist,peak_calc(psdarray, i))
    return peaklist

# Superimpose peak_calc onto analysis
def peak_impose(ax, frequency, peaklist):
    x = list(range(len(peaklist)))
    ax2 = ax.twinx()
    gf.std_graph(ax2, frequency[x], peaklist, c = 'b')

if __name__ == '__main__':
    filename = sys.argv[1]
    audio = aa.load_npy(filename)
    f, psd = aa.spectrum(audio)
    ax = gf.init_image()
    gf.semi_graph(ax, f, psd, label = filename)
    maxdex = aa.max_range(psd, 20)
    # print(f)
    gf.button_grapher(ax, f, maxdex, psd)
    peaklist = peak_map(psd)
    peak_impose(ax, f, peaklist)
    plt.show()
