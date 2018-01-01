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

# Given npy array, convert into frequency domain
def spectrum(audio, frequency = 44100):
    f, psd = signal.welch(audio, 44100, nperseg = 1024, window = 'hamming')
    # f = f[:-80]
    # psd = psd[:-80]
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
    # bluecurve = bluecurve * curve[500]/bluecurve[500]
    snratio = bluecurve/curve

    # Graph ax
    semi_graph(ax, freq, curve, label = 'background')
    semi_graph(ax, freq, bluecurve, 'b', 'recording')
    std_graph(ax2, freq, snratio, label = 'S/N ratio')
    ax.legend(loc=2)
    ax2.legend(loc=0)

    plt.show()
