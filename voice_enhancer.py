import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile 
from file_process import *

def y_freq_max():
    x_freq, y_freq = show_freq_domain('asset/new_record/newhappy.wav')
    maxAmp = np.argmax(y_freq)
    return maxAmp

def enhance(x_freq, start_freq, end_freq):

    bounds = list()

    for i in range(len(x_freq)):
        if x_freq[i] < 85:
            bounds.append(i)
            break 

    for i in range(len(x_freq)):
        if x_freq[i] > start_freq:
            bounds.append(i)
            break
            
    for i in range(len(x_freq)):
        if x_freq[i] > end_freq:
            bounds.append(i)
            break
    
    for i in range(len(x_freq)):
        if x_freq[i] > 2000:
            bounds.append(i)
            break 

    wave_data, nchannels, sample_width, framerate, numframes = read_file('asset/new_record/newhappy.wav')
    wave_data_fre = np.fft.fft(wave_data)

    start = bounds[0]
    start_voice = bounds[1]
    end_voice = bounds[2]
    end = bounds[3]

    wave_data_fre[start_voice:end_voice] = wave_data_fre[start_voice:end_voice] * 10
    wave_data_fre[int(len(wave_data_fre)-end_voice):int(len(wave_data_fre)-start_voice)] = wave_data_fre[int(len(wave_data_fre)-end_voice):int(len(wave_data_fre)-start_voice)] * 10
    
    wave_data_fre[start:start_voice] = wave_data_fre[start:start_voice] / 2
    wave_data_fre[int(len(wave_data_fre)-start_voice):int(len(wave_data_fre)-start)] = wave_data_fre[int(len(wave_data_fre)-start_voice):int(len(wave_data_fre)-start)] / 2

    wave_data_fre[end:-1] = wave_data_fre[end:-1] / 2
    wave_data_fre[1:int(len(wave_data_fre)-end)] = wave_data_fre[1:int(len(wave_data_fre)-end)] / 2

    after_enhance = np.fft.ifft(wave_data_fre)
    clr = np.real(after_enhance)
    enhanced_audio = clr.astype(np.int16)
    wavfile.write('enhance.wav', framerate, enhanced_audio)
    
if __name__ == '__main__':
    
    enhance(x_freq,85,y_freq_max())
    
    


