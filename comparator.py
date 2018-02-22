#!/usr/bin/env python3
import numpy as np
import os, sys
sys.path.append('/Users/aperocky/workspace/Labwork/Drone_Project/Audio-detection/engines')
import graph_functions as gf
import audio_algorithms as aa
from matplotlib import pyplot as plt

#---------------------------------------------------------------------------#
''' Purpose of this script is to compare the two recorded audios. Preferably,
one of them will be the background, the other the audio of interest. '''
#---------------------------------------------------------------------------#

# Prints the maximums on each
def print_maxdex(fs, power, maxdex):
    for each in maxdex:
        print('On bin %d, Maximum Frequency at %.01f Hz, POWER OVER BACKGROUND %.01f times' % (each, fs[each], power[each]))

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
    background = aa.load_npy(background)
    audio = aa.load_npy(audio)
    ax = gf.init_image()

    # Set double scale
    ax2 = ax.twinx()

    # Run spectrum analysis
    freq, curve = aa.spectrum(background, fs)
    _, bluecurve = aa.spectrum(audio, fs)
    # bluecurve = bluecurve * curve[2]/bluecurve[2]
    snratio = bluecurve/curve

    # Graph ax
    gf.semi_graph(ax, freq, curve, label = 'background')
    gf.semi_graph(ax, freq, bluecurve, 'b', 'recording')
    gf.std_graph(ax2, freq, snratio, label = 'S/N ratio')
    maxdex = aa.max_range(bluecurve, 10)
    print_maxdex(freq, snratio, maxdex)
    gf.pin_grapher(ax, freq, maxdex, curve, bluecurve)
    ax.legend(loc=2)
    ax2.legend(loc=0)
    plt.show()
