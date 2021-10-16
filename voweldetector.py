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


def divide_wav_file(file_path, time_slot):
    """
    Splitting audio files into time_slot spaced files and write into 'temp' folder to further FFT operation
    :param file_path: Original wav file path
    :param time_slot: Time period to be intercepted, second as unit
    :return: None
    """
    # open original wav file
    f = wave.open(file_path, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)
    f.close()

    wave_data = np.frombuffer(str_data, dtype=np.short)
    # data process depending on the number of channels
    if nchannels > 1:
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        temp_data = wave_data.T
    else:
        wave_data = wave_data.T
        temp_data = wave_data.T

    # Number of frames in one time slot
    frames_num = framerate * time_slot
    # Number of slot
    slot_num = nframes / frames_num
    frames_num_int = int(frames_num)

    # Determine if 'temp' folder exists
    if not os.path.exists('temp/'):
        # Create 'temp' folder if not exist
        os.makedirs('temp/')

    for j in range(int(math.ceil(slot_num))):
        current_file_name = "../temp/slot" + "-" + str(j) + ".wav"
        current_slot_data = temp_data[int(frames_num_int * j):int(frames_num_int * j + frames_num)]
        current_slot_data.shape = 1, -1
        current_slot_data = current_slot_data.astype(np.short)
        f = wave.open(current_file_name, 'wb')
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(current_slot_data.tostring())
        f.close()


def fft_operation(file_path):
    """
    FFT operation
    :param file_path:
    :return:
    """
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    divide_wav_file('asset/new_record/newhappy.wav', 0.2)

    # read files under the temp folder
    path = r"temp"
    files = os.listdir(path)
    files = [path + "/" + f for f in files if f.endswith('.wav')]

    # Store the highest frequency of current file
    sen_freqs = list()
    for i in range(len(files)):
        time_i, slot_fft_i = fft_operation(files[i])
        sen_freqs.append(time_i[int(np.argmax(slot_fft_i))])
    sen_freqs.sort()

    print(sen_freqs)

    # Store frequency of different vowels
    vowel_freqs = dict()

    # FFT operation of different vowel audio files
    time_1, slot_fft_1 = fft_operation('asset/new_record/e.wav')
    time_2, slot_fft_2 = fft_operation('asset/new_record/i.wav')
    time_3, slot_fft_3 = fft_operation('asset/new_record/er.wav')
    time_4, slot_fft_4 = fft_operation('asset/new_record/wu.wav')
    time_5, slot_fft_5 = fft_operation('asset/new_record/u.wav')
    time_6, slot_fft_6 = fft_operation('asset/new_record/o.wav')

    vowel_freqs['e'] = (time_1[int(np.argmax(slot_fft_1))])
    vowel_freqs['i'] = (time_2[int(np.argmax(slot_fft_2))])
    vowel_freqs['er'] = (time_3[int(np.argmax(slot_fft_3))])
    vowel_freqs['wu'] = (time_4[int(np.argmax(slot_fft_4))])
    vowel_freqs['u'] = (time_5[int(np.argmax(slot_fft_5))])
    vowel_freqs['o'] = (time_6[int(np.argmax(slot_fft_6))])

    print(vowel_freqs)

    '''
    Store the score which defines as 1 - distance between different sentences' highest frequency and vowels' frequency
    e.g.
        A: sentence_1's highest frequency
        B: vowel /æ/'s frequency
        score = 1 - abs( A - B )
    '''
    scores = dict()
    for k, v, in vowel_freqs.items():
        temp_list = list()
        for idx in range(len(sen_freqs)):
            value = sen_freqs[idx] / v
            '''
            Due to the fact that some frequency is higher than 1e2 even more, so we define that if frequency is higher 
            than 1.3e2, we use the decimals
            '''
            if value > 1.3:
                value = math.modf(value)[0]
            temp_list.append(value)

        # Get the score
        for i in range(len(temp_list)):
            if temp_list[i] < 1:
                temp_list[i] = 1 - temp_list[i]
            else:
                temp_list[i] = temp_list[i] - 1
        temp_list.sort(reverse=False)
        scores[k] = temp_list[0]

    print('score(distance to 100%): \n', scores)

    # Plot vowels' frequency
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
