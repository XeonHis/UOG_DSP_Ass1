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
    
    x_time, y_time = show_time_domain('asset/new_record/newhappy.wav')
    x_freq, y_freq = show_freq_domain('asset/new_record/newhappy.wav')
    
   
    
    # plt.figure(figsize=(40, 20))
    plt.subplot(3, 1, 1)
    plt.plot(x_time, y_time)
    # plt.plot(sliced_time, sliced_normalized_wave_data)
    plt.title('Time Domain')
    plt.xlabel('Time')
    plt.ylabel('Normalised amplitudes')
    plt.subplot(3, 1, 2)
    plt.plot(x_freq, y_freq)
    plt.title('Frequency Domain')
    plt.xlabel('Frequency')
    plt.ylabel('')

    
    
    enhance(x_freq,50,100)

    x_freq, y_freq = show_freq_domain('enhance.wav')
    plt.subplot(3, 1, 3)
    plt.plot(x_freq, y_freq)
    plt.title('After enhance')
    plt.xlabel('Frequency')
    plt.ylabel('')
    plt.show() 
    

