# frequency of sine wave: 440Hz
# frequency of æ: 107Hz
# frequency of eɪ: 613Hz
# frequency of ɜː: 118.9Hz
# frequency of happy: peak_1 = 131Hz, peak_2 = 667Hz
# frequency of E: 126Hz
import matplotlib.pyplot as plt
import numpy as np
import math

from file_process import *


# todo: 分段成小slot进行fft
def detect_original_frequency(file_path):
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    sen_time, sen_fft = detect_original_frequency('asset/new_record/pi.wav')
    ai_time, ai_fft = detect_original_frequency('asset/sound_æ.wav')
    i_time, i_fft = detect_original_frequency('asset/new_record/i.wav')
    wu_time, wu_fft = detect_original_frequency('asset/new_record/wu.wav')
    u_time, u_fft = detect_original_frequency('asset/new_record/u.wav')

    plt.subplot(3, 2, 1)
    plt.plot(sen_time, sen_fft)

    plt.subplot(3, 2, 2)
    plt.plot(ai_time, ai_fft)

    plt.subplot(3, 2, 3)
    plt.plot(i_time, i_fft)

    plt.subplot(3, 2, 4)
    plt.plot(wu_time, wu_fft)

    plt.subplot(3, 2, 5)
    plt.plot(u_time, u_fft)

    plt.show()
