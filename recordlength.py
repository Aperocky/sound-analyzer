import os, sys
cdir = os.getcwd()
sys.path.append(cdir)
import record
import sounddevice as sd

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('not enough arguments')
    filename = sys.argv[1]
    time_length = int(sys.argv[2])
    record.record(filename=filename, time = time_length)
    nparray = record.load(filename)
    sd.play(ndarray)
