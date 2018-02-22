import numpy as np
import os, sys
sys.path.append('/Users/aperocky/workspace/Labwork/Drone_Project/Audio-detection/engines')
import harmonics
import audio_algorithms as aa

def splinters(fname, numparts):
    diskdata = np.load(fname)
    length = len(diskdata) - numparts
    length = int(length/numparts)
    i = 0
    datas = []
    while(i < numparts):
        newdata = diskdata[i*length: (i+1)*length]
        datas.append(newdata)
        i += 1
    result = []
    for each in datas:
        harmonic = harmonics.run(each)
        identify = aa.identify(harmonic)
        result.append(identify)
    return result

if __name__ == '__main__':
    fname = sys.argv[1]
    numparts = int(sys.argv[2])
    result = splinters(fname, numparts)
    print(result)
