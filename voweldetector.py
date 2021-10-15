# frequency of sine wave: 440Hz
# frequency of æ: 107Hz
# frequency of eɪ: 613Hz
# frequency of ɜː: 118.9Hz
# frequency of happy: peak_1 = 131Hz, peak_2 = 667Hz
# frequency of E: 126Hz
import matplotlib.pyplot as plt
import numpy as np
import math
import os

from file_process import *


def divide_wav_file(file_path):
    pass


def detect_original_frequency(file_path):
    # 74752, 1, 2, 44100, 74752
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    divide_wav_file(None)

    path = r"temp"
    files = os.listdir(path)
    files = [path + "/" + f for f in files if f.endswith('.wav')]
    # print(len(files))
    sen_freqs = list()
    for i in range(len(files)):
        time_i, slot_fft_i = detect_original_frequency(files[i])
        # print(time_i[int(np.argmax(slot_fft_i))])
        sen_freqs.append(time_i[int(np.argmax(slot_fft_i))])
    sen_freqs.sort()
    print(sen_freqs)

    vowel_freqs = dict()
    time_1, slot_fft_1 = detect_original_frequency('asset/new_record/e.wav')
    time_2, slot_fft_2 = detect_original_frequency('asset/new_record/i.wav')
    time_3, slot_fft_3 = detect_original_frequency('asset/new_record/er.wav')
    time_4, slot_fft_4 = detect_original_frequency('asset/new_record/wu.wav')
    time_5, slot_fft_5 = detect_original_frequency('asset/new_record/u.wav')
    time_6, slot_fft_6 = detect_original_frequency('asset/new_record/o.wav')

    vowel_freqs['e'] = (time_1[int(np.argmax(slot_fft_1))])
    vowel_freqs['i'] = (time_2[int(np.argmax(slot_fft_2))])
    vowel_freqs['er'] = (time_3[int(np.argmax(slot_fft_3))])
    vowel_freqs['wu'] = (time_4[int(np.argmax(slot_fft_4))])
    vowel_freqs['u'] = (time_5[int(np.argmax(slot_fft_5))])
    vowel_freqs['o'] = (time_6[int(np.argmax(slot_fft_6))])

    print(vowel_freqs)

    scores = dict()

    for k, v, in vowel_freqs.items():
        temp_list = list()
        for idx in range(len(sen_freqs)):
            value = sen_freqs[idx] / v
            if value > 1.3:
                value = math.modf(value)[0]
            temp_list.append(value)

        for i in range(len(temp_list)):
            if temp_list[i] < 1:
                temp_list[i] = 1 - temp_list[i]
            else:
                temp_list[i] = temp_list[i] - 1
        temp_list.sort(reverse=False)
        scores[k] = temp_list[0]

    print('score(distance to 100%): \n', scores)

    plt.subplot(2, 3, 1)
    plt.plot(time_1, slot_fft_1)
    plt.title('e')
    plt.xlim(0, 600)

    plt.subplot(2, 3, 2)
    plt.plot(time_2, slot_fft_2)
    plt.title('i')
    plt.xlim(0, 600)

    plt.subplot(2, 3, 3)
    plt.plot(time_3, slot_fft_3)
    plt.title('er')
    plt.xlim(0, 600)

    plt.subplot(2, 3, 4)
    plt.plot(time_4, slot_fft_4)
    plt.title('wu')
    plt.xlim(0, 600)

    plt.subplot(2, 3, 5)
    plt.plot(time_5, slot_fft_5)
    plt.title('u')
    plt.xlim(0, 600)

    plt.subplot(2, 3, 6)
    plt.plot(time_6, slot_fft_6)
    plt.title('o')
    plt.xlim(0, 600)

    plt.show()
