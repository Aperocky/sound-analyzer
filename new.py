import numpy as np
import os, sys
sys.path.append('/Users/aperocky/workspace/Labwork/Drone_Project/Audio-detection/engines')
import audio_algorithms as aa
import graph_functions as gf

audio1 = aa.load_npy('10m_0m_0.npy')
audio2 = aa.load_npy('10m_2m_0.npy')
audio3 = aa.load_npy('10m_4m_0.npy')
audio4 = aa.load_npy('10m_6m_0.npy')
audio5 = aa.load_npy('10m_10m_0.npy')
bandpass = [80, 10000]
f, psd1 = aa.spectrum(audio1, bandpass = bandpass)
f, psd2 = aa.spectrum(audio2, bandpass = bandpass)
f, psd3 = aa.spectrum(audio3, bandpass = bandpass)
f, psd4 = aa.spectrum(audio4, bandpass = bandpass)
f, psd5 = aa.spectrum(audio5, bandpass = bandpass)
ax = gf.init_image()
gf.semi_graph(ax, f, psd1, c='r')
gf.semi_graph(ax, f, psd2, c='b')
gf.semi_graph(ax, f, psd3, c='g')
gf.semi_graph(ax, f, psd4, c='y')
gf.semi_graph(ax, f, psd5, c='k')
# maxdex = aa.max_range(psd, 20)
# peaklist = aa.peak_map(psd)
# plt.savefig('%s.png' % filename.split('.')[0])
gf.show()
