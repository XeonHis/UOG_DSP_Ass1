import scipy.fftpack
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import wave
import struct


def show_time_domain(file_path):
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

    time = np.linspace(0, numframes / framerate, numframes)
    max_wave = np.max(wave_data)
    normalized_wave_data = wave_data / max_wave
    time_length = len(time)
    normalized_wave_data_length = len(normalized_wave_data)
    # sliced time & normalized wave data
    sliced_time = time[int(0.5 * time_length):int(0.9 * time_length)]
    sliced_normalized_wave_data = normalized_wave_data[
                                  int(0.5 * normalized_wave_data_length):int(0.9 * normalized_wave_data_length)]

    plt.plot(time, normalized_wave_data)
    # plt.plot(sliced_time, sliced_normalized_wave_data)
    plt.title('Time Domain')
    plt.xlabel('Time')
    plt.ylabel('Normalised amplitudes')
    plt.show()


def show_freq_domain(file_path):
    epsilon = 1e-30
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

    # print(wave_data)
    fft = np.fft.fft(wave_data)
    abs_fft = np.abs(fft)
    print(np.argmax(abs_fft))
    freqs = np.linspace(0, framerate, numframes)
    freqs_length = len(freqs)
    abs_fft_length = len(abs_fft)

    plt.plot(np.log(freqs + epsilon), np.log(abs_fft + epsilon))
    # plt.plot(np.log(freqs[int(0.6*freqs_length):int(0.61*freqs_length)]+epsilon), np.log(abs_fft[int(0.6*abs_fft_length):int(0.61*abs_fft_length)]+epsilon))
    plt.title('Frequency Domain')
    plt.xlabel('Frequency')
    plt.ylabel('')
    plt.show()


if __name__ == '__main__':
    # show_time_domain('asset/sound_æ.wav')
    show_freq_domain('asset/sound_æ.wav')
