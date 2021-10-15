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


def divide_wav_file(file_path):
    origAudio = wave.open(file_path, 'r')
    frameRate = origAudio.getframerate()
    nChannels = origAudio.getnchannels()
    sampWidth = origAudio.getsampwidth()
    nframes = origAudio.getnframes()
    wave_data = origAudio.readframes(nframes)

    time_slot = 1
    slot_frames = int(time_slot * frameRate)
    start = 0
    # print(math.ceil(nframes / slot_frames))

    for i in range(math.ceil(nframes / slot_frames)+1):
        num = start + slot_frames
        print(num)
        if (num) < nframes:
            current_wave_data = wave_data[start:start + slot_frames]
        else:
            current_wave_data = wave_data[start:nframes + 1]

        chunkAudio = wave.open('temp/slot_' + str(i) + '.wav', 'w')
        chunkAudio.setnchannels(nChannels)
        chunkAudio.setsampwidth(sampWidth)
        chunkAudio.setframerate(frameRate)
        chunkAudio.writeframes(current_wave_data)
        chunkAudio.close()

        start = start + slot_frames


def detect_original_frequency(file_path):
    # 74752, 1, 2, 44100, 74752
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)
    # todo: 分段成小slot进行fft

    # time_slot = 0.02
    # slot_frames = int(time_slot * framerate)
    # start = 0
    # for i in range(math.ceil(numframes / slot_frames)):
    #     if start + slot_frames < numframes:
    #         current_wave_data = wave_data[start:start + slot_frames]
    #     else:
    #         current_wave_data = wave_data[start:numframes]
    #     current_abs_fft = np.abs((np.fft.fft(current_wave_data)))
    #     current_normalized_fft = current_abs_fft / len(current_wave_data)
    #     half_fft = 2 * current_normalized_fft[range(int(len(current_wave_data) / 2))]
    #     freqs = np.linspace(0, framerate, slot_frames)
    #
    #     # slot = np.fft.ifft(cur)
    #     # clr = np.real(enhance)
    #     # audio = clr.astype(np.int16)
    #     # wavfile.write('slot_' + str(i) + '.wav', framerate, current_wave_data)
    #
    #     start = start + slot_frames
    #
    #     # plt.plot(freqs[:int(len(freqs) / 2)], half_fft)
    #     max_wave_idx = np.argmax(half_fft)
    #     freqs = freqs[:int(len(freqs) / 2)]
    #     max_wave_freq = freqs[int(max_wave_idx)]
    #     print('idx:', max_wave_idx, '  freq:', max_wave_freq)

    # abs_fft = np.abs(np.fft.fft(wave_data))
    # normalized_abs_fft = abs_fft / len(wave_data)
    # half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    # freqs = np.linspace(0, framerate, numframes)
    #
    # return freqs[:int(len(freqs) / 2)], 20 * np.log10(half_fft / np.max(half_fft))


if __name__ == '__main__':
    divide_wav_file('asset/new_record/newhappy.wav')
    # detect_original_frequency('asset/new_record/moment.wav')

    plt.show()
