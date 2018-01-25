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
# print(data)

# Generate Statistics

# AVERAGE OF POWER LEVELS ACROSS 130 - 170 HZ FOR EACH INTERVAL
av_data = np.sum(data[:,:,1], axis = 1)/data.shape[1]
print('Average of each interval:\n', av_data)

# AVERAGE OF THE AVERAGE OF POWER LEVELS
av_av_data = np.sum(av_data[1:])/(len(av_data)-1)
print('Average of averages: %.02f' % av_av_data)

# STANDARD DEVIATION OF THE POWER LEVELS FOR EACH INTERVAL
std_data = np.std(data[:,:,1], axis = 1)
print('Standard Deviation of each interval:\n', std_data)

# AVERAGE OF STANDARD DEVIATION OF POWER LEVELS
av_std_data = np.sum(std_data[1:])/(len(std_data)-1)
print('Average of standard deviations of POWER: %.02f' % av_std_data)

# AVERAGE OF MATCHES IN EACH INTERVAL
av_match = np.sum(data[:,:,2], axis = 1)/160
print('Average of matches in each interval\n', av_match)

# AVERAGE OF AVERAGES OF MATCHES IN EACH INTERVAL
av_av_match = np.sum(av_match[1:])/(len(av_match)-1)
print('Average of averages of matches: %.02f' % av_av_match)

# STANDARD DEVIATION OF THE MATCH FOR EACH INTERVAL
std_match = np.std(data[:,:,2], axis = 1)
print('Standard Deviation of matches in each interval:\n', std_match)

# AVERAGE OF STANDARD DEVIATION OF MATCHES
av_std_match = np.sum(std_match[1:])/(len(std_match)-1)
print('Average of standard deviations of MATCHES: %.02f' % av_std_match)

for each in data:
    result = aa.identify(each)
    aa.print_identify(result)
