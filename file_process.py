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
        left = val[0:2]
        # right = val[2:4]
        v = struct.unpack('h', left)[0]
        wave_data[i] = v
    return wave_data, nchannels, sample_width, framerate, numframes


def show_time_domain(file_path):
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    time = np.linspace(0, numframes / framerate, numframes)
    max_wave = np.max(wave_data)
    normalized_wave_data = wave_data / max_wave
    time_length = len(time)
    normalized_wave_data_length = len(normalized_wave_data)
    # sliced time & normalized wave data
    sliced_time = time[int(0.5 * time_length):int(0.9 * time_length)]
    sliced_normalized_wave_data = normalized_wave_data[
                                  int(0.5 * normalized_wave_data_length):int(0.9 * normalized_wave_data_length)]
    return time, normalized_wave_data


def show_freq_domain(file_path):
    epsilon = 1e-30
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)
    # print(wave_data)
    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)
    return freqs[:int(len(freqs)/2)], half_fft

<<<<<<< Updated upstream
=======
    plt.plot(freqs[:int(len(freqs) / 2)], half_fft)
>>>>>>> Stashed changes

if __name__ == '__main__':
    x_time, y_time = show_time_domain('asset/vowel_A.wav')
    x_freq, y_freq = show_freq_domain('asset/vowel_A.wav')
    plt.figure(figsize=(40, 20))
    plt.subplot(2,1,1)
    plt.plot(x_time, y_time)
    # plt.plot(sliced_time, sliced_normalized_wave_data)
    plt.title('Time Domain')
    plt.xlabel('Time')
    plt.ylabel('Normalised amplitudes')
    plt.subplot(2,1,2)
    plt.plot(x_freq, y_freq)
    plt.title('Frequency Domain')
    plt.xlabel('Frequency')
    plt.ylabel('')
    plt.show()
