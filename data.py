#!/usr/bin/env python3
import numpy as np
import os, sys
sys.path.append('/Users/aperocky/workspace/Labwork/Drone_Project/Audio-detection/engines')
import graph_functions as gf
import audio_algorithms as aa
import harmonics
import fftfreq
import matplotlib.pyplot as plt

# # Load Data
# filename = sys.argv[1]
# data = np.load(filename)
# # print(data)
#
# # Generate Statistics
#
# # AVERAGE OF POWER LEVELS ACROSS 130 - 170 HZ FOR EACH INTERVAL
# av_data = np.sum(data[:,:,1], axis = 1)/data.shape[1]
# print('Average of each interval:\n', av_data)
#
# # AVERAGE OF THE AVERAGE OF POWER LEVELS
# av_av_data = np.sum(av_data[1:])/(len(av_data)-1)
# print('Average of averages: %.02f' % av_av_data)
#
# # STANDARD DEVIATION OF THE POWER LEVELS FOR EACH INTERVAL
# std_data = np.std(data[:,:,1], axis = 1)
# print('Standard Deviation of each interval:\n', std_data)
#
# # AVERAGE OF STANDARD DEVIATION OF POWER LEVELS
# av_std_data = np.sum(std_data[1:])/(len(std_data)-1)
# print('Average of standard deviations of POWER: %.02f' % av_std_data)
#
# # AVERAGE OF MATCHES IN EACH INTERVAL
# av_match = np.sum(data[:,:,2], axis = 1)/160
# print('Average of matches in each interval\n', av_match)
#
# # AVERAGE OF AVERAGES OF MATCHES IN EACH INTERVAL
# av_av_match = np.sum(av_match[1:])/(len(av_match)-1)
# print('Average of averages of matches: %.02f' % av_av_match)
#
# # STANDARD DEVIATION OF THE MATCH FOR EACH INTERVAL
# std_match = np.std(data[:,:,2], axis = 1)
# print('Standard Deviation of matches in each interval:\n', std_match)
#
# # AVERAGE OF STANDARD DEVIATION OF MATCHES
# av_std_match = np.sum(std_match[1:])/(len(std_match)-1)
# print('Average of standard deviations of MATCHES: %.02f' % av_std_match)

fname = sys.argv[1]
# index = 0
# result = []
# while(True):
#     if not os.path.isfile('%s%d.npy' % (fname, index)):
#         break
#     data = np.load('%s%d.npy' % (fname, index))
#     print('%dTH    ' % index, end=' ')
#     # fftfreq.run('%s%d.npy' % (fname, index))
#     if index == 50:
#         break
#     intervaldata = harmonics.run(data)
#     intervaldata = aa.identify(intervaldata)
#     print(intervaldata)
#     result.append(intervaldata)
#     index += 1

gen = aa.split_seconds(fname)
result = []
for each in gen:
    intervaldata = harmonics.run(each)
    intervaldata = aa.identify(intervaldata)
    result.append(intervaldata)
result = np.asarray(result)
print(result)

def plotdots(ax, i, detect):
    colored = 'r'
    if detect:
        colored = 'b'
    gf.std_graph(ax, [i, i+1], [0, 0], c=colored, lw = 3)

print(np.average(result[:, 2]) - 120)
print(np.average(result[:, 3]))

ax = gf.init_image(xlabel = 'Intervals', ylabel = 'Power Rating', title = '')
ax.set_ylim(-10, 200)
i = 0
tot = 0
for each in result:
    print(each)
    print(aa.detect(each))
    if aa.detect(each):
        tot += 1
    plotdots(ax, i, aa.detect(each))
    i += 1
print(tot)
gf.std_graph(ax, np.arange(len(result)), result[:, 2] - 120, c='g', label = 'Power')
# ax.axvspan(4, 21, alpha=0.5, color='b')
# ax.axvspan(30, 51, alpha=0.5, color='b')
# ax.axvspan(65, 72, alpha=0.5, color='b')
# ax.axvspan(3, 16, alpha=0.5, color='b')
# ax.axvspan(33, 54, alpha=0.5, color='b')
# ax.axvspan(11, 36, alpha=0.5, color='b')
# ax.axvspan(55, 72, alpha=0.5, color='b')
ax2 = gf.get_twinx(ax, ylabel = 'Matches')
gf.std_graph(ax2, np.arange(len(result)), result[:, 3], c='r', label = 'Matches')
ax.legend(loc = 2)
ax2.legend(loc = 1)
gf.show()
