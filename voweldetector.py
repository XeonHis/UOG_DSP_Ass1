# frequency of sine wave: 440Hz
# frequency of æ: 107Hz
# frequency of eɪ: 613Hz
# frequency of ɜː: 118.9Hz
# frequency of happy: peak_1 = 131Hz, peak_2 = 667Hz
# frequency of E: 126Hz

from file_process import *


def detect_original_frequency(file_path):
    wave_data, nchannels, sample_width, framerate, numframes = read_file(file_path)

    # print(wave_data)
    abs_fft = np.abs(np.fft.fft(wave_data))
    normalized_abs_fft = abs_fft / len(wave_data)
    half_fft = 2 * normalized_abs_fft[range(int(len(wave_data) / 2))]
    freqs = np.linspace(0, framerate, numframes)

    plt.plot(freqs[:int(len(freqs) / 2)], half_fft)

    plt.title('Frequency Domain')
    plt.xlabel('Frequency')
    plt.ylabel('')
    plt.show()


if __name__ == '__main__':
    detect_original_frequency('asset/sound_happy.wav')
