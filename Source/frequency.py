# Filename: frequency.py
#
# Summary: reads wav files
#
# Author: Samuel Villavicencio
# 
# Last Updated: Oct 07 2015

import sys		# exit argv
import time		# time
import wave		# open getframerate getnchannels getsampwidth getnframes readframes error
import numpy		# empty uint8 fromstring shape reshape view
import traceback	# format_exc
import scipy.signal	# fftconvolve
import matplotlib.mlab	# difference

# OCTAVES represents the frequency bounds of every octave
# BASE_FR represents the individual frequencies in the 0th octave
# BASE_NO represents the musical notation of the base frequencies
OCTAVES = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034.0, 4068.0, 7902.0]
BASE_FR = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
BASE_NO = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']

def read(filename):
	''' Read and prepare the audio file. '''
	
	# try to extract attributes from wav file.
	try:
		wav = wave.open(filename)
		sample_rate = wav.getframerate()
		channels = wav.getnchannels()
		sampwidth = wav.getsampwidth()
		frames = wav.getnframes()
		signal = wav.readframes(frames)
		no_samples, remainder = divmod(len(signal), sampwidth * channels)

		# if there are more than one channels - stereo - average them.
		if( channels > 1 ):
			actual = ''
			for (sample1, sample2) in zip(signal[0::2], signal[1::2]):
				actual += hex((ord(sample1) + ord(sample2)) / 2)[2:].zfill(2).decode('hex')
			signal = actual
			no_samples /= 2

		# create numpy array to represent signal string as appropriate data type
		# according to the sample width.
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
		raise IOError
		sys.exit(1)

	except wave.Error:
		raise wave.Error
		sys.exit(1)

	return signal, sample_rate
	
def findFrequency(signal, sample_rate):
	''' Determine the frequency of the signal. '''

	# correct the signal.
	signal = scipy.signal.fftconvolve(signal, signal[::-1], mode='full')
	signal = auto[len(auto)/2:]

	# find the first minimum point in the signal.
	difference = numpy.diff(signal)
	start = matplotlib.mlab.find(difference > 0)[0]
    
	# find the peak from that position.
	peak = numpy.argmax(signal[start:]) + start

	# calculate the period using parabolic interpolation.
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
	frequency = frequency / (2 ** octave)
	
	# get the letter note of the frequency.
	for index in range(12):
		if(abs(BASE_FR[index] - frequency) < .6):
			note = BASE_NO[index]
			break
	
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
