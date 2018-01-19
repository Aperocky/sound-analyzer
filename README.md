# sound-analyzer

This project folder contains several very useful scripts that may be extended to general sound frequency analysis, all is written in python3

Currently, it's my project interest to analyze the sound made by drones, but the tools does not restrict itself to any certain type of sounds.

## <code>recordlength.py</code>

This script is designed to record audio data into numpy arrays (float arrays). With microphone hooked up to the default input, <code>sounddevice</code> module will be used to convert audio input into numpy arrays.

The script takes in two[,three] arguments, in following order:

<code>recordlength.py filename length[ fs]</code>

<code>filename</code> is a string where you wish where the final saved file would end up.

<code>length</code> is an int which describe how many seconds this recording will be.

<code>fs</code> is optional, where you specify the sampling frequency, the default sampling frequency is 44100.

## <code>analyze.py</code>

This script is a very simple analyzer utilizing signal welch and matplotlib to effectively transform audio data into frequency space. it will show a red line for the audio data being analyzed. Peak will be labeled based on my preliminary peak finding algorithm.

To run: <code>analyze.py filename</code>

<code>filename</code> is a string pointing to the data file you want to analyze. default frequency is 44100.

## <code>analyze_time.py</code>

This script will take audio data and analyze its frequency as parts of time - this will be useful to analyze data
