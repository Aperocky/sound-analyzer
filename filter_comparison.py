import numpy as np
import os, sys
thisdir = os.path.abspath('engines')
sys.path.append(thisdir)
import audio_algorithms as aa
import graph_functions as gf
from scipy.signal import butter, lfilter

# Generate f, psd from data:
def procdata(data, bandpass):
    data = aa.bandpass_filter(data, bandpass)
    f, psd = aa.spectrum(data, bandpass = bandpass)
    return f, psd

# Generate multiple curves on same data and save all of it.
def datagen(filename):
    psdlists = []
    for each in aa.split_seconds(filename):
        f, psd = procdata(each, [80, 2000])
        # gf.just_plot(f, psd)
        psdlists.append(psd)
    psdlist = np.asarray(psdlists)
    return f, psd

# Generate a background curve from big data.
def background(f, psd):
    

# data = np.load('soundfiles/Trial0107/50ft_0ft_0.npy')
# freq = aa.bandpass_filter(data, [80, 2000])
# gf.just_plot(np.arange(len(freq)), freq, std=True)

datagen('Trial0209_0/20m100s_0.npy')
