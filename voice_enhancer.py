import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile 
from file_process import *


def enhance(x_freq, start_freq, end_freq):

    bounds = list()
    for i in range(len(x_freq)):
        if x_freq[i] > start_freq:
            bounds.append(i)
            break
            
    for i in range(len(x_freq)):
        if x_freq[i] > end_freq:
            bounds.append(i)
            break
    
    wave_data, nchannels, sample_width, framerate, numframes = read_file('asset/new_record/newhappy.wav')
    wave_data_fre = np.fft.fft(wave_data)
    start = bounds[0]
    end = bounds[-1]
    wave_data_fre[start:end] = wave_data_fre[start:end] * 10
    wave_data_fre[int(len(wave_data_fre)-end):int(len(wave_data_fre)-start)] = wave_data_fre[int(len(wave_data_fre)-end):int(len(wave_data_fre)-start)]*10
    enhance = np.fft.ifft(wave_data_fre)
    clr = np.real(enhance)
    audio = clr.astype(np.int16)
    wavfile.write('enhance.wav', framerate, audio)
    
   
if __name__ == '__main__':
    
    x_freq, y_freq = show_freq_domain('asset/new_record/newhappy.wav')
    enhance(x_freq, 0, 2)

