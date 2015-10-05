import sys
import time
import wave
import numpy
import traceback
import scipy.signal
import matplotlib.mlab
import matplotlib.pyplot

OCTAVES = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034.0, 4068.0, 7902.0]
BASE_FR = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
BASE_NO = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']

def read(filename):
	''' Read the audio file and return the raw signal, sample rate and number of channels. '''
	
	# try to extract raw signal and other attributes from wav file.
	try:
		wav = wave.open(filename)
		sample_rate = wav.getframerate()
		channels = wav.getnchannels()
		sampwidth = wav.getsampwidth()
		frames = wav.getnframes()
		signal = wav.readframes(frames)
		no_samples, remainder = divmod(len(signal), sampwidth * channels)
		# if there are more than one channels - stereo - average them.
		# algorithm source https://stackoverflow.com/questions/20677390/python-wave-byte-data#answer-20677733
		if( channels > 1 ):
			actual = ''
			for (sample1, sample2) in zip(signal[0::2], signal[1::2]):
				actual += hex((ord(sample1) + ord(sample2)) / 2)[2:].zfill(2).decode('hex')
			signal = actual
			no_samples /= 2
		# create numpy array to represent signal string as appropriate data type.
		# if the audio has a bit depth of 24 bits, reshape the data to fit 32 bits.
		# algorithm source https://gist.github.com/WarrenWeckesser/7461781
		if(sampwidth == 3):
			array = numpy.empty((no_samples, channels, 4), dtype = numpy.uint8)
			raw_bytes = numpy.fromstring(signal, dtype=numpy.uint8)
			array[:, :, :sampwidth] = raw_bytes.reshape(-1, channels, sampwidth)
			array[:, :, sampwidth:] = (array[:, :, sampwidth - 1:sampwidth] >> 7) * 255
			signal = array.view('<i4').reshape(array.shape[:-1])
			signal = signal.reshape(-1)
		else:
			if(sampwidth == 1):
				dt_char = 'u'
			else:
				dt_char = 'i'
			array = numpy.fromstring(signal, dtype = '<%s%d' % (dt_char, sampwidth))
			signal = array.reshape(-1)
	except IOError:
		print 'Error: Cannot open %s' % filename
		print traceback.format_exc()
		sys.exit(0)
		
	return signal, sample_rate
	
def graph(signal, sample_rate):
	''' Plot the signal. '''
	
	# plot with respect to time.
#	Time = numpy.linspace(0, len(signal) / sample_rate, num = len(signal))
#	matplotlib.pyplot.plot(Time, signal)

	# plot with respect to the number of samples.
	matplotlib.pyplot.plot(signal)
	matplotlib.pyplot.show()

def autocorrelate(signal):
	''' Autocorrelate the signal. '''

	# create third signal using Fast Fourier Transform 
	# and convolution of the signal and itself.
	# remove the negative lag.
	auto = scipy.signal.fftconvolve(signal, signal[::-1], mode='full')
	auto = auto[len(auto)/2:]
	
	return auto

def findFrequency(signal, sample_rate):
	''' Determine the frequency of the signal. '''

	# algorithm source https://gist.github.com/endolith/255291
	# find the first minimum point in the signal.
	difference = numpy.diff(signal)
	start = matplotlib.mlab.find(difference > 0)[0]
    
	# find the peak from that position.
	# calculate the period using quadratic interpolation.
	peak = numpy.argmax(signal[start:]) + start
	period = 1/2.0 * (signal[peak-1] - signal[peak+1]) / (signal[peak-1] - 2 * signal[peak] + signal[peak+1]) + peak
    
	return (sample_rate / period)

def recognize(frequency):
	''' Match the frequency to the musical note. '''
	
	# get the octave of the frequency.
	for index, value in enumerate(OCTAVES):
		if(frequency < value):
			octave = index
			break

	# adjust the frequency.
	adj_freq = frequency / (2 ** octave)
	
	# get the letter note of the frequency.
	for index in range(12):
		if(abs(BASE_FR[index] - adj_freq) < .6):
			note = BASE_NO[index]
			break
			
	# abjad readable note / octave combination.
	note = note + str(octave)
	return note

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print 'Usage: python %s <filename>' % sys.argv[0]
		sys.exit(1)
	else:
		audio = []
		for index in range(1, len(sys.argv)):
			audio.append(str(sys.argv[index]))
	
		for filename in audio:
			start_time = time.time()
			signal, sample_rate = read(filename)
			auto = autocorrelate(signal)
			freq = findFrequency(auto, sample_rate)
			print '******************************'
			print 'Number of Samples: %i' % len(signal)
			print 'Sample rate: %i' % sample_rate
			print 'Frequency: %.3f' % freq
			print 'Note: %s' % recognize(freq)
			print 'Time elapsed: %.3f s' % (time.time() - start_time)
