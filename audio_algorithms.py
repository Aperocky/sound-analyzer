import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal

# Load numpy (audio) files
def load_npy(filename):
    return np.load(filename)

# Given audio, transform the data onto the frequency space with welch function.
def spectrum(audio, frequency = 44100):
    f, psd = signal.welch(audio, frequency, nperseg = 4096, window = 'hamming')
    cutoff = 500
    f = f[:cutoff]
    psd = psd[:cutoff]
    # print(psd)
    return f, psd

# Find local maximums in an array
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

# Old fft algorithm before using welch algorithm
def fft(nparray):
    freq = np.fft.fft(nparray)
    half = np.arange(1,len(freq)/2+1,dtype=int)
    freq = freq[100:-100]
    nfreq = np.zeros(len(freq), dtype=complex)
    nfreq[100:-100] = freq
    psd = np.sqrt(np.abs((nfreq[half])**2 + (nfreq[-half])**2))
    return psd
