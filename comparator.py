#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from matplotlib import pyplot as plt

''' Purpose of this script is to compare the two recorded audios. Preferably,
one of them will be the background, the other the audio of interest. '''

# Load files by FILENAME
def load_npy(filename):
    return np.load(filename)

# Initiate pyplot image
def init_image():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_xlabel('Frequency: Hz')
    ax.set_ylabel('Power Density')
    return ax

# Given a graph, plot it onto the ax object
def semi_graph(ax, x, y, c = 'r', label = ''):
    ax.semilogy(x,y, color=c, label = label)

def std_graph(ax, x, y, c = 'g', label = ''):
    ax.plot(x,y, color=c, label = label)

def pin_grapher(ax, frequency, maxdex, background, audio):
    for each in maxdex:
        vert = frequency[each]
        ax.plot([vert, vert], [background[each], audio[each]], color='k')
        ax.text(vert, audio[each], 'Peak at %.0f' % vert)

def max_in_range(data, interval):
    leng = len(data)
    maxdex = set()
    for i in range(leng - interval):
        local = data[i:i+interval]
        index = np.argmax(local) + i
        maxdex.add(index)
    return maxdex

# Improved version of max_in_range
def max_range(data, interval):
    leng = len(data)
    maxdex = set()
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
            maxdex.add(index)
    return maxdex

# Helper function for improved max_range
def discard_max(interval, amax, threshold = 1.5):
    minimum = np.min(interval)
    if amax/minimum < threshold:
        return True
    return False

def print_maxdex(fs, power, maxdex):
    for each in maxdex:
        print('On bin %d, Maximum Frequency at %.01f Hz, POWER OVER BACKGROUND %.01f times' % (each, fs[each], power[each]))

# Given npy array, convert into frequency domain
def spectrum(audio, frequency = 44100):
    f, psd = signal.welch(audio, frequency, nperseg = 4096, window = 'hamming')
    cutoff = 1400
    f = f[10:-cutoff]
    psd = psd[10:-cutoff]
    # print(psd)
    return f, psd

if __name__ == '__main__':
    # Default argument block
    if len(sys.argv) < 3:
        sys.exit('not enough arguments')
    background = sys.argv[1]
    audio = sys.argv[2]
    fs = 44100
    if len(sys.argv) > 3:
        fs = int(sys.argv[3])

    # Build image
    background = load_npy(background)
    audio = load_npy(audio)
    ax = init_image()

    # Set double scale
    ax2 = ax.twinx()

    # Run spectrum analysis
    freq, curve = spectrum(background, fs)
    _, bluecurve = spectrum(audio, fs)
    # bluecurve = bluecurve * curve[2]/bluecurve[2]
    snratio = bluecurve/curve

    # Graph ax
    semi_graph(ax, freq, curve, label = 'background')
    semi_graph(ax, freq, bluecurve, 'b', 'recording')
    std_graph(ax2, freq, snratio, label = 'S/N ratio')
    maxdex = max_range(bluecurve, 10)
    print_maxdex(freq, snratio, maxdex)
    pin_grapher(ax, freq, maxdex, curve, bluecurve)
    ax.legend(loc=2)
    ax2.legend(loc=0)

    plt.show()
