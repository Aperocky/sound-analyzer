import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import splinter

name = '200ft_100m_'
alist = np.arange(10)
result = []
for each in alist:
    namestr = '%s%d.npy' % (name, each)
    if os.path.exists(namestr):
        subres = splinter.splinters(namestr, 3)
        result.extend(subres)

result = np.asarray(result)
print(result)
np.save('%sresults1' % name, result)
