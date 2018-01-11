#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from matplotlib import pyplot as plt

def load_npy(filename):
    return np.load(filename)

def spectrum(audio, frequency = 44100):
    f, psd = signal.welch(audio, frequency, nperseg = 4096, window = 'hamming')
    cutoff = 500
    f = f[:cutoff]
    psd = psd[:cutoff]
    # print(psd)
    return f, psd

# Improved version of max_in_range
def max_range(data, interval):
    leng = len(data)
    maxdex = list()
    middle = int(interval/2)
    for i in range(leng - interval):
        # Padding increases the range as frequency increases
        padding = int(i/50)
        if i+interval+padding < leng:
            local = data[i-padding:i+interval+padding]
        else:
            break
        localmax = np.max(local)
        if discard_max(local, localmax):
            continue
        if data[i+middle] == localmax:
            index = i + middle
            maxdex.append(index)
    return maxdex

# Helper function for improved max_range
def discard_max(interval, amax, threshold = 1.5):
    minimum = np.min(interval)
    if amax/minimum < threshold:
        return True
    return False

# Initiate pyplot image
def init_image():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_xlabel('Frequency: Hz')
    ax.set_ylabel('Power Density')
    return ax

def pin_grapher(ax, frequency, maxdex, audio):
    print(maxdex)
    ax.scatter(frequency[maxdex], audio[maxdex], c= 'b')
    for each in maxdex:
        ax.text(frequency[each], audio[each], 'Peak at %.0f' % frequency[each])

# Given a graph, plot it onto the ax object
def semi_graph(ax, x, y, c = 'r', label = ''):
    ax.semilogy(x,y, color=c, label = label)

if __name__ == '__main__':
    filename = sys.argv[1]
    audio = load_npy(filename)
    f, psd = spectrum(audio)
    ax = init_image()
    semi_graph(ax, f, psd, label = filename)
    maxdex = max_range(psd, 20)
    # print(f)
    pin_grapher(ax, f, maxdex, psd)
    plt.show()
