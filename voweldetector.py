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


def detect_original_frequency(file_path):
    # 74752, 1, 2, 44100, 74752
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)
    # todo: 分段成小slot进行fft
    time_slot = 0.02
    slot_frames = int(time_slot * framerate)
    start = 0
    for i in range(math.ceil(numframes / slot_frames)):
        if start + slot_frames < numframes:
            current_wave_data = wave_data[start:start + slot_frames]
        else:
            current_wave_data = wave_data[start:numframes]
        current_abs_fft = np.abs((np.fft.fft(current_wave_data)))
        current_normalized_fft = current_abs_fft / len(current_wave_data)
        half_fft = 2 * current_normalized_fft[range(int(len(current_wave_data) / 2))]
        freqs = np.linspace(0, framerate, slot_frames)

        start = start + slot_frames

        # plt.plot(freqs[:int(len(freqs) / 2)], half_fft)
        max_wave_idx = np.argmax(half_fft)
        freqs = freqs[:int(len(freqs) / 2)]
        max_wave_freq = freqs[max_wave_idx]
        print('idx:', max_wave_idx, '  freq:', max_wave_freq)
        # print(freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft)))

    # abs_fft = np.abs(np.fft.fft(wave_data))
    # normalized_abs_fft = abs_fft / len(wave_data)
    # half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    # freqs = np.linspace(0, framerate, numframes)
    #
    # return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    sen_time, sen_fft = detect_original_frequency('asset/new_record/newhappy.wav')

    plt.show()
