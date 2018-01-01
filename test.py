import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import sys

def record(filename = '', time=10, fs=44100):
    duration = time
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking = True)
    print(recording)
    # recording1 = recording[:,0]
    # recording1 = recording1[20000:]
    # plt.plot(recording1)
    # sd.play(recording1, fs, blocking= True)
    # plt.show()
    if filename == '':
        save('tempvoice', recording)
    else:
        save(filename, recording)
    return recording

def save(outfile, nparray):
    np.save(outfile, nparray)

def load(outfile):
    return np.load(outfile)

def fft(nparray):
    freq = np.fft.fft(nparray)
    half = np.arange(1,len(freq)/2+1,dtype=int)
    freq = freq[100:-100]
    nfreq = np.zeros(44100, dtype=complex)
    nfreq[100:-100] = freq
    psd = np.sqrt(np.abs((nfreq[half])**2 + (nfreq[-half])**2))
    return psd

# save('outfile.sd')
# record = load('outfile.sd.npy')
# print(len(record))
#
# recordlist = np.split(record, 10)
# for each in recordlist[:2]:
#     window = np.hamming(44100)
#     plt.plot(1/window)
#     plt.show()
#     # plt.plot(window)
#     # plt.show()
#     # print(len(each))
#     each = each*window
#     freq = np.fft.fft(each)
#     half = np.arange(1,len(freq)/2+1,dtype=int)
#     freq = freq[100:-100]
#     nfreq = np.zeros(44100, dtype=complex)
#     nfreq[100:-100] = freq
#     # print(nfreq)
#     psd = np.sqrt(np.abs((nfreq[half])**2 + (nfreq[-half])**2))
#     # plt.plot(np.real(np.fft.ifft(nfreq)))
#     # plt.plot(each)
#     plt.semilogy(psd[0:400], 'k-')
#     plt.show()
#     sd.play(np.real(np.fft.ifft(nfreq)), blocking=True)

if __name__ == '__main__':
    whatever = input('Press Start: ')
    record = record(time=1)
    plt.figure(1)
    plt.plot(record)
    plt.show()
    plt.figure(2)
    psd = fft(record)
    plt.plot(psd[100:1000])
    plt.show()
    pass


# print(len(recording1))
# a = np.fft.fft(recording1, n=5000)
# print(a)
# plt.plot(recording1)
# # plt.plot(a)
# plt.show()
