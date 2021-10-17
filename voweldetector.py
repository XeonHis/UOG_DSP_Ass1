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
import shutil

from file_process import *


def divide_wav_file(file_path, time_slot):
    """
    Splitting audio files into time_slot spaced files and write into 'temp' folder to further FFT operation
    :param file_path: Original wav file path
    :param time_slot: Time period to be intercepted, second as unit
    :return: the relative path of the audio file
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
        current_file_name = "temp/slot" + "-" + str(j) + ".wav"
        current_slot_data = temp_data[int(frames_num_int * j):int(frames_num_int * j + frames_num)]
        current_slot_data.shape = 1, -1
        current_slot_data = current_slot_data.astype(np.short)
        f = wave.open(current_file_name, 'wb')
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(current_slot_data.tostring())
        f.close()
    return file_path


def fft_operation(file_path):
    """
    FFT operation
    :param file_path: Original wav file path
    :return: freqs, 20 * log10(fft/max_fft), name
    """
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft)), file_path[file_path.rfind(
        '/') + 1:file_path.find('.')]


def compare_freqs(file_path):
    """
    Compare frequency between sentences and vowels to generate the score
    :return:
    """
    # read files under the temp folder
    path = r"temp"
    files = os.listdir(path)
    files = [path + "/" + f for f in files if f.endswith('.wav')]

    # Store the highest frequency of current file
    sen_freqs = list()
    for i in range(len(files)):
        freq_i, slot_fft_i, _ = fft_operation(files[i])
        sen_freqs.append(freq_i[int(np.argmax(slot_fft_i))])
    sen_freqs.sort()

    # print(sen_freqs)

    # Store frequency of different vowels
    vowel_freqs = dict()

    # FFT operation of different vowel audio files
    freq_ei, slot_fft_ei, name_ei = fft_operation('asset/vowel/ei.wav')
    freq_i, slot_fft_i, name_i = fft_operation('asset/vowel/i.wav')
    freq_er, slot_fft_er, name_er = fft_operation('asset/vowel/er.wav')
    freq_wu, slot_fft_wu, name_wu = fft_operation('asset/vowel/wu.wav')
    freq_u, slot_fft_u, name_u = fft_operation('asset/vowel/u.wav')
    freq_o, slot_fft_o, name_o = fft_operation('asset/vowel/o.wav')
    freq_ai, slot_fft_ai, name_ai = fft_operation('asset/vowel/ai.wav')
    freq_uh, slot_fft_uh, name_uh = fft_operation('asset/vowel/uh.wav')
    freq_e, slot_fft_e, name_e = fft_operation('asset/vowel/e.wav')

    vowel_freqs['ei'] = (freq_ei[int(np.argmax(slot_fft_ei))])
    vowel_freqs['i'] = (freq_i[int(np.argmax(slot_fft_i))])
    vowel_freqs['er'] = (freq_er[int(np.argmax(slot_fft_er))])
    vowel_freqs['wu'] = (freq_wu[int(np.argmax(slot_fft_wu))])
    vowel_freqs['u'] = (freq_u[int(np.argmax(slot_fft_u))])
    vowel_freqs['o'] = (freq_o[int(np.argmax(slot_fft_o))])
    vowel_freqs['ai'] = (freq_ai[int(np.argmax(slot_fft_ai))])
    vowel_freqs['uh'] = (freq_uh[int(np.argmax(slot_fft_uh))])
    vowel_freqs['e'] = (freq_e[int(np.argmax(slot_fft_e))])

    # print(vowel_freqs)

    '''
    Store the score which defines as 1 - distance between different sentences' highest frequency and vowels' frequency
    e.g.
        A: sentence_1's highest frequency
        B: vowel /æ/'s frequency
        score = 1 - A / B
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

    print('score(distance to 100%): ', sorted(scores.items(), key=lambda x: x[1], reverse=False))

    # We set threshold as 4%, if distance to 100% is lower than threshold, it means the vowel is in the sentence
    threshold = 0.04
    output_vowels = dict()
    score_list = sorted(scores.items(), key=lambda x: x[1], reverse=False)
    for i in range(len(score_list)):
        if float(score_list[i][1]) < threshold:
            output_vowels[score_list[i][0]] = score_list[i][1]
    output_vowels_list = list(output_vowels.keys())

    # Phonetic transcription of vowels
    vowel_tostring = dict()
    vowel_tostring['ei'] = '/ei/'
    vowel_tostring['i'] = '/ɪ/'
    vowel_tostring['er'] = '/ɜː/'
    vowel_tostring['wu'] = '/u:/'
    vowel_tostring['u'] = '/juː/'
    vowel_tostring['o'] = '/ɔ:/'
    vowel_tostring['ai'] = '/aɪ/'
    vowel_tostring['uh'] = '/ʌ/'
    vowel_tostring['e'] = '/iː/'
    # print(list(output_vowels.keys()))
    print('\nThese vowels are in sentences (' + file_path + '): ', end='')
    for i in range(len(output_vowels_list)):
        print(vowel_tostring[output_vowels_list[i]], end=' ')

    return [(freq_ei, slot_fft_ei, name_ei), (freq_i, slot_fft_i, name_i), (freq_er, slot_fft_er, name_er),
            (freq_wu, slot_fft_wu, name_wu), (freq_u, slot_fft_u, name_u), (freq_o, slot_fft_o, name_o),
            (freq_ai, slot_fft_ai, name_ai), (freq_uh, slot_fft_uh, name_uh), (freq_e, slot_fft_e, name_e)]


def show_figures(time_and_frequency):
    """
    Show figures of vowels' frequency
    :param time_and_frequency: list, contains (frequency, fft_data, name)
    :return: None
    """
    length = len(time_and_frequency)
    row = math.floor(math.sqrt(length))
    col = math.ceil(math.sqrt(length))
    for i in range(length):
        # Plot vowels' frequency
        plt.subplot(row, col, i + 1)
        plt.plot(time_and_frequency[i][0], time_and_frequency[i][1])
        plt.title(time_and_frequency[i][-1])
        plt.xlim(0, 600)

    plt.show()


if __name__ == '__main__':
    # 2 arguments: audio file path, time interval
    freq_list = compare_freqs(divide_wav_file('asset/sentences/sentence3.wav', 0.1))
    # Remove temp file
    shutil.rmtree('temp/')
    show_figures(freq_list)
