import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from matplotlib import pyplot as plt


def fft(nparray):
    freq = np.fft.fft(nparray)
        half = np.arange(1,len(freq)/2+1,dtype=int)
    freq = freq[100:-100]
    nfreq = np.zeros(len(freq), dtype=complex)
    nfreq[100:-100] = freq
    psd = np.sqrt(np.abs((nfreq[half])**2 + (nfreq[-half])**2))
    return psd

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('not enough arguments')
    filename = sys.argv[1]
    fs = 44100
    if not len(sys.argv) < 3:
        fs = int(sys.argv[2])
    soundarray = np.load(filename)
    # sd.play(soundarray, 4410)
    intervals = np.split(soundarray, int(len(soundarray)/4410))
    # intervals = intervals[::3]
    for each in intervals:
        each = each[:, 0]
        # print(len(each))
        f, psd = signal.welch(each, fs, nperseg = 256, window = 'hamming')
        print(psd)
        plt.plot(f[10:], psd[10:])
        plt.show()
        plt.close()

    f, psd = signal.welch(soundarray[:, 0], fs, nperseg = 1024, window = 'hamming')
    plt.plot(f[10:], psd[10:])
    plt.show()
    plt.close()
