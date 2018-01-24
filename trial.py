import numpy as np
import sys

filename = sys.argv[1]
data = np.load(filename)
print(data)
print(data.shape)
