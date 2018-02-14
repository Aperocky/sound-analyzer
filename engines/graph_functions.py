import sounddevice as sd
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
from scipy import signal
from matplotlib import pyplot as plt

# Load numpy (audio) files
def load_npy(filename):
    return np.load(filename)

# Initiate pyplot image with ax.
def init_image(xlabel = '', ylabel = '', title = ''):
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def just_plot(x, y, label = '', std = False, linewidth = 1, c='g', xlabel = '', ylabel = '', title = ''):
    ax = init_image()
    if std:
        std_graph(ax, x, y, c = c, label = label, lw = linewidth)
    else:
        semi_graph(ax, x, y, c = c, label = label)
    plt.show()

# Get the twinx
def get_twinx(ax, ylabel = ''):
    ax2 = ax.twinx()
    ax2.set_ylabel(ylabel = ylabel)
    # ax2.grid(True)
    return ax2

# Given a graph, plot it onto the ax object in a semilog way
def semi_graph(ax, x, y, c = 'r', label = ''):
    ax.semilogy(x,y, color=c, label = label)

# Given a graph, plot it onto the ax object in a standard way
def std_graph(ax, x, y, c = 'g', label = '', lw = 1):
    ax.plot(x,y, color=c, label = label, linewidth=lw)

# Graph points based on index and array. (frequency[maxdex] = index, audio = array)
def button_grapher(ax, frequency, maxdex, audio):
    # print(maxdex)
    ax.scatter(frequency[maxdex], audio[maxdex], c= 'b')
    for each in maxdex:
        ax.text(frequency[each], audio[each], 'Peak at %.0f' % frequency[each])

# Graph horizontal lines based on index, topline and bottomline.
def pin_grapher(ax, frequency, maxdex, background, audio):
    for each in maxdex:
        vert = frequency[each]
        ax.plot([vert, vert], [background[each], audio[each]], color='k')
        ax.text(vert, audio[each], 'Peak at %.0f' % vert)

def show():
    plt.show()
