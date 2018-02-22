import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from operator import itemgetter
from scipy.signal import butter, lfilter
import graph_functions as gf

'''---------------------------UTILITY FUNCTIONS------------------------------'''

# Load numpy (audio) files
def load_npy(filename):
    return np.load(filename)

# Split an file into multiple parts
def split_files(filename, num):
    data = np.load(filename)
    totallength = int(len(data)/44100)
    segmentlength = int(totallength/num)
    i = 0
    while(i < num - 1):
        split = data[i*segmentlength*44100: (i+1)*segmentlength*44100]
        print(len(split))
        np.save('{}_{}'.format(filename, i), split)
        i += 1
    np.save('{}_{}'.format(filename, i), data[i*segmentlength*44100:])

# Have a generator that yield seperate files from one master file.
def split_seconds(filename, length = 44100*4, split_length = 44100):
    data = np.load(filename, 'r')
    totallength = len(data)
    i = 0
    while(i*split_length + length < totallength):
        split = np.asarray(data[i*split_length: i*split_length+length])
        i += 1
        yield split

'''---------------------------WELCH ALGORITHM--------------------------------'''

# Given audio, transform the data onto the frequency space with welch function.
def spectrum(audio, frequency = 44100, bandpass = []):
    f, psd = signal.welch(audio, frequency, nperseg = 4096, window = 'hamming')
    f, psd = filter_frequency(f, psd, bandpass, frequency)
    return f, psd

# Filter the f, psd to contain only the frequencies.
def filter_frequency(f, psd, bandpass, fs = 44100):
    if len(bandpass) == 0:
        return f, psd
    left = bandpass[0]
    right = bandpass[1]
    inlef = np.searchsorted(f, left)
    inrte = np.searchsorted(f, right, side='right')
    f = f[inlef: inrte]
    psd = psd[inlef: inrte]
    return f, psd

'''---------------------------BANDPASS FILTERING-----------------------------'''

# Generate bandpass filters
def butter_bandpass(lowcut, highcut, fs, order=9):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, bandpass, fs = 44100, order = 3):
    b, a = butter_bandpass(bandpass[0], bandpass[1], fs, order)
    data = lfilter(b, a, data)
    return data

'''---------------------------FIND MAX IN PEAK RANGE-------------------------'''

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

'''------------------INDIVIDUAL FFT OF SHORTER PERIOD OF TIME----------------'''

# Old fft algorithm before using welch algorithm
def fft(nparray, fs):
    ham = np.hamming(len(nparray))
    nparray = nparray * ham
    freq = np.fft.rfft(nparray)
    freq = freq[:-1]
    nfreq = np.real(freq)
    psd = nfreq**2
    psd = welchlocal(psd)
    multitude = fs/len(nparray)
    f = (np.arange(len(nparray))+1)*multitude
    return psd

# Sooth the fft frequency using some averaging function.
def welchlocal(psd):
    leng = len(psd)
    newleng = int(leng/5)
    psd = psd[:newleng+6]
    welch = []
    i = 0
    while(i < newleng):
        if i < 5:
            welch.append(np.sum(psd[i:i+5]))
        elif i > newleng:
            welch.append(np.sum(psd[i-5:i]))
        else:
            welch.append(np.sum(psd[i-2:i+3]))
        i += 1
    return welch

'''---------------------------PEAK CALCULATIONS------------------------------'''

def peak_calc(psdarray, index, irange):
    # irange is the range of interest.
    maxpeak = 10
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
    peakstrength = psdarray[index]**2/mincons/maxi
    if peakstrength > maxpeak:
        peakstrength = maxpeak
    return peakstrength

# Calculate Peak from long averages of base rather than local spectra.
def new_peak(psdarray, index, irange):
    if index < 20:
        averages = np.average(psdarray[:40])
    else:
        averages = np.average(psdarray[index-20:index+20])
    strength = psdarray[index]/averages
    return strength

# Map
def peak_map(psdarray, irange = 4):
    peaklist = np.zeros(irange + 2)
    for i in range(irange + 2,len(psdarray)-50):
        # peaklist = np.append(peaklist,new_peak(psdarray, i, irange))
        peaklist = np.append(peaklist,peak_calc(psdarray, i, irange))
    padding = np.zeros(50)
    peaklist = np.append(peaklist, padding)
    return peaklist

# Identify the peaks of the peaklist ..
def peak_assign(peaklist):
    peaks = []
    maxpeak = 10
    for i in range(len(peaklist)):
        if i < 5:
            continue
        if i > len(peaklist) - 5:
            break
        if peaklist[i] == maxpeak:
            peaks.append(i)
            continue
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
    gf.button_grapher(ax2, frequency, peaksdex, peaklist)

'''------------IDENTIFICATION OF DRONES USING HARMONICS DECISION-------------'''

# Identify a drone from the result of harmonics - CORE.
def identify(result):
    av_power = np.sum(result[:,1])/result.shape[0]
    av_match = np.sum(result[:,2])/result.shape[0]
    mask = result[:, 2] > av_match
    # print('%.02f' % av_match, end = ' ')
    if np.sum(mask) < 1:
        return False
    selected = result[mask]
    mask = selected[:, 1] > av_power
    if np.sum(mask) < 1:
        return False
    selected = selected[mask]
    quants = []
    for each in selected:
        quant = (each[1]) * each[2]
        quants.append((each[0], quant, each[1], each[2]))
    strong = max(quants, key=itemgetter(1))
    return strong

def detect(strong):
    metric = strong[2] + (strong[3] - 5)*10 - 120
    if metric > 40:
        return True
    return False

# Print out identify's output
def print_identify(result):
    if not result:
        print('No drone is detected')
    else:
        if 120 < result[0] < 170:
            print('Harmonics detected at %.02f Hz, Strength %.02f' % (result[0], result[2]-120))
        else:
            print('No drone is detected')
