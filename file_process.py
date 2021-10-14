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
    return np.log10(freqs[:int(len(freqs) / 2)]), 20 * np.log10(half_fft / np.max(half_fft))

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

    # x_time, y_time = show_freq_domain('asset/vowel_A.wav')
    # x_freq, y_freq = show_freq_domain('asset/vowel_E.wav')
    plt.figure(figsize=(20,60))
    x_time, y_time = show_time_domain('asset/new_record/newhappy.wav')
    x_freq, y_freq = show_freq_domain('asset/new_record/newhappy.wav')
    x_org_freq, y_org_freq = show_org_freq_domain('asset/new_record/newhappy.wav')
    # plt.figure(figsize=(40, 20))
    plt.subplot(3, 1, 1)
    plt.plot(x_time, y_time)
    plt.title('Time Domain')
    plt.xlabel('Time')
    plt.ylabel('Normalised amplitudes')
    plt.subplot(3, 1, 2)
    plt.plot(x_freq, y_freq)
    plt.title('Frequency Domain')
    plt.xlabel('Logged Frequency')
    plt.ylabel('Amplitudes')
    plt.subplot(3, 1, 3)
    plt.plot(x_org_freq, y_org_freq)
    plt.title('Frequency Domain')
    plt.xlabel('Origin Frequency')
    plt.ylabel('Amplitudes')
    plt.show()
