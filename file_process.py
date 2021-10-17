import scipy.fftpack
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import wave
import struct
import scipy.signal as signal


def read_file(file_path):
    wave_file = wave.open(file_path, 'rb')

    nchannels = wave_file.getnchannels()
    sample_width = wave_file.getsampwidth()
    framerate = wave_file.getframerate()
    numframes = wave_file.getnframes()

    wave_data = np.zeros(numframes)

    for i in range(numframes):
        val = wave_file.readframes(1)
        if len(val) >2:
            # left = val[0:2]
            right = val[2:4]
            v = struct.unpack('h', right)[0]
            wave_data[i] = v
        else:
            v = struct.unpack('h', val)[0]
            wave_data[i] = v
    return wave_data, nchannels, sample_width, framerate, numframes


def show_time_domain(file_path):
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    time = np.linspace(0, numframes / framerate, numframes)
    max_wave = np.max(wave_data)
    normalized_wave_data = wave_data / max_wave
    return time, normalized_wave_data



def show_freq_domain(file_path):

    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)
    # print(wave_data)
    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)
    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))



def show_org_freq_domain(file_path):
    epsilon = 1e-30
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)
    # print(wave_data)
    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)
    return freqs[:int(len(freqs) / 2)], half_fft / np.max(half_fft)

if __name__ == '__main__':

    #x_time, y_time = show_freq_domain('asset/seperate_hb/0.15.wav')
    # x_freq, y_freq = show_freq_domain('asset/vowel_E.wav')
    #plt.figure(figsize= (50,30))
    x_a1, y_a1 = show_org_freq_domain('asset/seperate_hb/0.196.wav')
    x_a2, y_a2 = show_org_freq_domain('asset/seperate_hb/0.875.wav')
    x_o1, y_o1 = show_org_freq_domain('asset/seperate_hb/1.183.wav')
    x_o2, y_o2 = show_org_freq_domain('asset/seperate_hb/1.373.wav')
    x_i, y_i = show_org_freq_domain('asset/seperate_hb/0.593.wav')
    x_u, y_u = show_org_freq_domain('asset/seperate_hb/1.425.wav')
    x_all, y_all = show_freq_domain('asset/new_record/newhappy.wav')

    # plt.figure(figsize=(40, 20))
    # plt.subplot(4, 2, 1)
    # plt.title("a1")
    # plt.plot(x_a1, y_a1)
    # plt.plot(96.2, 1, 'bo')
    # #a1 96.2
    # # plt.xlabel('A1-Frequency')
    # plt.ylabel('Normalised amplitudes')
    #
    # plt.subplot(4, 2, 2)
    # plt.title("a2")
    # plt.plot(x_a2 , y_a2 )
    # plt.plot(86.2, 1, 'bo')
    # #a2 86.2
    # # plt.xlabel('A2-Frequency')
    # plt.ylabel('Nmlz Amp')
    #
    # plt.subplot(4, 2, 3)
    # plt.title("o1")
    # plt.plot(x_o1 , y_o1 )
    # plt.plot(92.8, 1, 'bo')
    # #o1 92.8
    # # plt.xlabel('O1-Frequency')
    # plt.ylabel('Nmlz Amp')
    #
    # plt.subplot(4, 2, 4)
    # plt.title("o2")
    # plt.plot(x_o2 , y_o2 )
    # plt.plot(173, 1, 'bo')
    # #o2 173
    # # plt.xlabel('O2-Frequency')
    # plt.ylabel('Nmlz Amp')
    #
    # plt.subplot(4, 2, 5)
    # plt.title("i")
    # plt.plot(x_i , y_i )
    # plt.plot(416.8, 1, 'bo')
    # #i 416.8
    # # plt.xlabel('I-Frequency')
    # plt.ylabel('Nmlz Amp')
    #
    # plt.subplot(4, 2, 6)
    # plt.title("u")
    # plt.plot(x_u , y_u )
    # plt.plot(338, 1, 'bo')
    # #u 338
    # # plt.xlabel('U-Frequency')
    # plt.ylabel('Nmlz Amp')

    # plt.subplot(4, 2, 7)
    print(np.log10(96.2),20*np.log10(0.243))
    plt.figure(figsize=(15, 5))
    plt.plot(x_all[:1500], y_all[:1500])
    #ORG-- #a1 [96.2,0.243] #a2 [86.2,0.577] #o1 [92.8,] #o2 [173,] #i [416.8,] #u [338,]
    #plt.plot([96.2, 86.2, 92.8, 173, 416.8, 338],[0,0,0,0,0,0], 'bo')
    plt.plot([96.2],[20*np.log10(0.243)], 'bo')
    plt.xlabel('Origin Frequency')
    plt.ylabel('Nmlz Amp')

    plt.show()
