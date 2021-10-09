from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import wave


def show_time_domain(file_path):
    wave_file = wave.open(file_path, 'rb')
    params = wave_file.getparams()
    # nchannels=2, sampwidth=2, framerate=44100, nframes=416742,
    framerate, nframes = params[2: 4]

    data = wave_file.readframes(nframes)
    wave_file.close()
    wave_data = np.frombuffer(data, dtype=np.int32)
    time = np.arange(0, nframes) / framerate
    max_wave = wave_data.max()

    plt.plot(time, wave_data / max_wave)
    plt.show()


if __name__ == '__main__':
    show_time_domain('asset/sound1.wav')
