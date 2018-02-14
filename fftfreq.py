import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import audio_algorithms as aa
import graph_functions as gf
import matplotlib.pyplot as plt
import numpy as np
import harmonics
import analyze as az

def run(fname):
    diskdata = np.load(fname, 'r')
    intervallength = 8820
    def gen():
        i = 0
        while(intervallength * i < len(diskdata)-intervallength):
            data = np.asarray(diskdata[intervallength*i:intervallength*(i+1)])
            i += 1
            yield data

    generator = gen()
    psdlist = []
    for data in generator:
        psd = aa.fft(data)
        psdlist.append(psd)

    f = (np.arange(len(psdlist[0]))+1)*5
    ports = []
    for psd in psdlist:
        # az.runfromfft(f,psd)
        # harmonics.runfromfft_graph(f,psd)
        ports.append(harmonics.runfromfft(f,psd))

    ports = np.asarray([list(tups) for tups in ports])
    ports[:, 2] -= 120
    plt.hist(ports[:, 0], 16, weights=ports[:, 2])
    plt.show()

if __name__ == '__main__':
    fname = sys.argv[1]
    run(fname)
