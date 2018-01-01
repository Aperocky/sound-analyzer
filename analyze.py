#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def fft(nparray):
    freq = np.fft.fft(nparray)
    half = np.arange(1,len(freq)/2+1,dtype=int)
    freq = freq[100:-100]
    nfreq = np.zeros(len(freq), dtype=complex)
    nfreq[100:-100] = freq
    psd = np.sqrt(np.abs((nfreq[half])**2 + (nfreq[-half])**2))
    return psd

def split(nparray, npart = 1):
    if npart == 1:
        return [nparray]
    intervals = np.split(nparray, npart)
    return intervals

def spectrum(intervals):
    psdlist = []
    for each in intervals:
        if len(each.shape) > 1:
            each = each[:, 0]
        f, psd = signal.welch(each, fs, nperseg = 2048, window = 'hamming')
        frequency = f
        psdlist.append(psd)
    psdlist = np.asarray(psdlist)
    return frequency, psdlist

def get_max(nparray):
    last = nparray[0]
    current = nparray[1]
    maxlist = []
    for i in range(len(nparray)-2):
        if current > nparray[i] and current > last:
            if current > 1e-12:
                maxlist.append((i+1, current))
        last = current
        current = nparray[i]
    return maxlist

def init():
    global line, recordline
    return line, recordline

def update(i):
    global line, frequency, psdmatrix, text, recordline, ax
    text.set_text('Period ' + str(i))
    line.set_data(frequency, psdmatrix[i])
    maxlist = get_max(psdmatrix[i])
    # print(maxlist)
    # texts = []
    # for each in maxlist:
    #     freq = frequency[each[0]]
    #     texts.append(ax.text(freq, each[1]*3, 'Peak %.02f' % freq))
    return line, recordline

def checksource(soundarray):
    plt.plot(soundarray)
    plt.show()
    plt.close()

if __name__ == '__main__':

    # INPUT ARGUMENTS:
    # FILENAME :  file to be opened
    # fs :  Sampling rate of that file
    # npart :  Frames numbers for FFT(welch) analysis.
    if len(sys.argv) < 2:
        sys.exit('not enough arguments')
    filename = sys.argv[1]
    fs = 44100
    npart = 1
    background = ''
    background_select = 3
    if len(sys.argv) > 2:
        fs = int(sys.argv[2])
    if len(sys.argv) > 3:
        npart = int(sys.argv[3])
    if len(sys.argv) > 4:
        background = sys.argv[4]
    if len(sys.argv) > 5:
        background_select = int(sys.argv[5])

    # GET SOUND ARRAY
    soundarray = np.load(filename)
    if not background == '':
        base_soundarray = np.load(background)
        base_sound = spectrum([base_soundarray])[1][0]
    # checksource(soundarray)
    # checksource(base_soundarray)

    # SPLIT ARRAY INTO FRAMES:
    intervals = split(soundarray, npart=npart)

    # Calculate Spectrums in 2d matrix
    frequency, psdmatrix = spectrum(intervals)
    # if npart < len(soundarray)/fs:
    #     psdmatrix *= len(soundarray)/fs/npart

    # Noise information
    # checksource(base_sound)

    # print(frequency)
    # print(psdmatrix)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim([1e-13, 1e-3])
    ax.set_xlim([0,20000])
    ax.set_xlabel('Frequency: Hz')
    ax.set_ylabel('Loudness: (dB)')
    ax.grid(True)
    line, = ax.semilogy([],[])
    if not background == '':
        recordline, = ax.semilogy(frequency, base_sound, c='r')
    else:
        recordline = None
    text = ax.text(10000, 1e-5, '')

    anim = animation.FuncAnimation(fig, update, frames = npart, interval = 500, init_func = init)
    plt.show()
