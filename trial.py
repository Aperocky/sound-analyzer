import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import audio_algorithms as aa

fname = '200ft_200ft_'
result = np.load('%sresults.npy' % fname)
# b = np.load('%sresults1.npy' % fname)
# result = np.concatenate((result, b))
print(len(result))
for each in result:
    print(each)
    print(aa.detect(each))

print(np.average(result[:, 2]) - 120)
print(np.average(result[:, 3]))
