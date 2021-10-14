# frequency of sine wave: 440Hz
# frequency of æ: 107Hz
# frequency of eɪ: 613Hz
# frequency of ɜː: 118.9Hz
# frequency of happy: peak_1 = 131Hz, peak_2 = 667Hz
# frequency of E: 126Hz
import matplotlib.pyplot as plt
import numpy as np

from file_process import *


def detect_original_frequency(file_path):
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    # print(wave_data)
    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    xorder = np.argsort(-half_fft)
    # print('xorder = ', xorder)
    xworder = list()
    for x in xorder:
        xworder.append(freqs[x])
    fworder = list()
    for x in xorder:
        fworder.append(half_fft[x])

    # plt.plot(freqs[:int(len(freqs) / 2)], half_fft)
    #
    # plt.title('Frequency Domain')
    # plt.xlabel('Frequency')
    # plt.ylabel('')
    # plt.show()
    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    sen_time, sen_fft = detect_original_frequency('asset/new_record/sentence.wav')
    e_time, e_fft = detect_original_frequency('asset/new_record/e.wav')
    er_time, er_fft = detect_original_frequency('asset/new_record/er.wav')
    i_time, i_fft = detect_original_frequency('asset/new_record/i.wav')
    o_time, o_fft = detect_original_frequency('asset/new_record/o.wav')
    u_time, u_fft = detect_original_frequency('asset/new_record/u.wav')

    plt.subplot(3, 2, 1)
    plt.plot(sen_time, sen_fft)
    plt.xlim(0, 600)

    plt.subplot(3, 2, 2)
    plt.plot(e_time, e_fft)
    plt.xlim(0, 600)

    plt.subplot(3, 2, 3)
    plt.plot(er_time, er_fft)
    plt.xlim(0, 600)

    plt.subplot(3, 2, 4)
    plt.plot(i_time, i_fft)
    plt.xlim(0, 600)

    plt.subplot(3, 2, 5)
    plt.plot(o_time, o_fft)
    plt.xlim(0, 600)

    plt.subplot(3, 2, 6)
    plt.plot(u_time, u_fft)
    plt.xlim(0, 600)

    # happy_time, happy_fft = detect_original_frequency('asset/happy_birthday.wav')
    # æ_time, æ_fft = detect_original_frequency('asset/sound_æ.wav')
    # i_time, i_fft = detect_original_frequency('asset/new_record/i.wav')
    # ɜ_time, ɜ_fft = detect_original_frequency('asset/ɜː.wav')
    #
    # plt.subplot(2, 2, 1)
    # plt.plot(happy_time, happy_fft)
    # plt.xlim(0, 1500)
    #
    # plt.subplot(2, 2, 2)
    # plt.plot(æ_time, æ_fft)
    # plt.xlim(0, 1500)
    #
    # plt.subplot(2, 2, 3)
    # plt.plot(i_time, i_fft)
    # plt.xlim(0, 1500)
    #
    # plt.subplot(2, 2, 4)
    # plt.plot(ɜ_time, ɜ_fft)
    # plt.xlim(0, 1500)

    plt.show()
