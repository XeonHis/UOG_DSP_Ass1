from file_process import *

def find_highst_freq():
    """
    Find the highest harmonic voice frequencies
    :return: The value of Hertz corresponding to the highest frequency in freq_domain
     """
    x_freq, y_freq = show_freq_domain('original.wav')
    maxAmp = np.argmax(y_freq)
    return maxAmp

def enhance(x_freq, start_freq, end_freq):
    """ 
    Improve sound quality and reduce noise, and write the audio file after enhanced named 'enhance.wav'
    :param x_freq: X axis of frequency domain diagram
    :param start_freq: The beginning of the highest harmonic voice frequencies
    :param end_freq: The end of the highest harmonic voice frequencies
     """

    # Delimit human voice area and noise area
    bounds = list()

    for i in range(len(x_freq)):
        # 85 is the lowest Hertz value of human sound
        if x_freq[i] > 20:
            bounds.append(i)
            break 

    for i in range(len(x_freq)):
        if x_freq[i] > start_freq:
            bounds.append(i)
            break
            
    for i in range(len(x_freq)):
        if x_freq[i] > end_freq:
            bounds.append(i)
            break
    
    for i in range(len(x_freq)):
        # 2000 is the highst Hertz value of human sound
        if x_freq[i] > 2000:
            bounds.append(i)
            break 

    # Read wavfile and fft opration
    wave_data, nchannels, sample_width, framerate, numframes = read_file('original.wav')
    wave_data_fre = np.fft.fft(wave_data)

    start = bounds[0]
    start_voice = bounds[1]
    end_voice = bounds[2]
    end = bounds[3]

    # Increase the region of the highest harmonic voice frequency amplitudes
    wave_data_fre[start_voice:end_voice] = wave_data_fre[start_voice:end_voice] * 10
    wave_data_fre[int(len(wave_data_fre)-end_voice):int(len(wave_data_fre)-start_voice)] = wave_data_fre[int(len(wave_data_fre)-end_voice):int(len(wave_data_fre)-start_voice)] * 10
    
    # Lower the frequency of other parts
    wave_data_fre[start:start_voice] = wave_data_fre[start:start_voice] / 2
    wave_data_fre[int(len(wave_data_fre)-start_voice):int(len(wave_data_fre)-start)] = wave_data_fre[int(len(wave_data_fre)-start_voice):int(len(wave_data_fre)-start)] / 2

    wave_data_fre[end:-1] = wave_data_fre[end:-1] / 2
    wave_data_fre[1:int(len(wave_data_fre)-end)] = wave_data_fre[1:int(len(wave_data_fre)-end)] / 2

    # Ifft opration and write file 
    after_enhance = np.fft.ifft(wave_data_fre)
    clr = np.real(after_enhance)
    enhanced_audio = clr.astype(np.int16)
    wavfile.write('improved.wav', framerate, enhanced_audio)
    
if __name__ == '__main__':

    x_freq, y_freq = show_freq_domain('original.wav')
    enhance(x_freq, 85, find_highst_freq())
    
    


