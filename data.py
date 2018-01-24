#!/usr/bin/env python3
import numpy as np
import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import graph_functions as gf
import audio_algorithms as aa

# Load Data
filename = sys.argv[1]
data = np.load(filename)

# Remove first data which is anomalous
print(data)

# Generate Statistics

# AVERAGE OF POWER LEVELS ACROSS 130 - 170 HZ FOR EACH INTERVAL
av_data = np.sum(data[:,:,1], axis = 1)/160
print('Average of each interval\n', av_data)

# AVERAGE OF THE AVERAGE OF POWER LEVELS
av_av_data = np.sum(av_data[:1])/(len(av_data)-1)
print('Average of averages: %d' % av_av_data)

# STANDARD DEVIATION OF THE POWER LEVELS FOR EACH INTERVAL
std_data = np.std(data[:,:,1], axis = 1)
print('Standard Deviation of each interval:\n', std_data)

# STANDARD DEVIATION OF THE MATCH FOR EACH INTERVAL
std_match = np.std(data[:,:,2], axis = 1)
print('Standard Deviation of matches in each interval:\n', std_match)
