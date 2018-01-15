import os,wave, audioop, sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
def downsampleWav(src, dst, inrate=44100, outrate=16000, inchannels=2, outchannels=1):
    if not os.path.exists(src):
        print('Source not found!')
        return False

    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
            
    except:
        print('Failed to open files!')
        return False
    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1:
            converted = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print('Failed to downsample wav')
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted)
    except:
        print('Failed to write wav')
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print('Failed to close wav files')
        return False
    return True
#input_arguments = sys.argv[1:]
#import_file = input_arguments[0]
import_file = "C:\\Users\\Admin\\Desktop\\test_data\\Giraffe.wav"
temp_read = wave.open(import_file,"r")
num_channels = temp_read.getnchannels()
sampling_rate = temp_read.getframerate()
output_temp = import_file[:import_file.index(".")] + "_output.wav"
downsampleWav(import_file,output_temp,sampling_rate, 16000, num_channels, 1)
spf = wave.open(output_temp,'r')
#Extract Raw Audio from Wav File
signal_temp = spf.readframes(-1)
signal_temp = np.fromstring(signal_temp, np.short)
signal_temp = signal_temp.astype(np.long)
test = scipy.signal.wiener(signal_temp,9,0.5*np.var(signal_temp))
s_write = wave.open(output_temp[:output_temp.index(".")] + "_filtered_output.wav", 'w')
s_write.setparams((1, 2, 16000, 0, 'NONE', 'Uncompressed'))
s_write.writeframes(test.astype(np.short).tostring())
s_write.close()
plt.figure(1)
plt.title('Signal Wave Original...')
plt.plot(signal_temp.astype(np.long))
plt.savefig("C:\\Users\\Admin\\Desktop\\test_data\\test.png")
plt.figure(2)
plt.title('Signal Wave Filtered...')
plt.plot(test.astype(np.long))
plt.savefig("C:\\Users\\Admin\\Desktop\\test_data\\origin.png")
