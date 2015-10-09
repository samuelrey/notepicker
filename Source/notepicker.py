# Filename: notepicker.py
#
# Summary: reads wav files
#
# Author: Samuel Villavicencio
# 
# Last Updated: Oct 07 2015

import os
import sys		# exit argv
import time		# time
import wave		# open getframerate getnchannels getsampwidth getnframes readframes error
import numpy		# empty uint8 fromstring shape reshape view
import traceback	# format_exc
import scipy.signal	# fftconvolve
import matplotlib.mlab	# difference

class NotePicker():
	def __init__(self):		
		# OCTAVES represents the frequency bounds of every octave
		# BASE_FR represents the individual frequencies in the 0th octave
		# BASE_NO represents the musical notation of the base frequencies
		self.OCTAVES = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034.0, 4068.0, 7902.0]
		self.BASE_NO = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']
		self.BASE_FR = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
		self.note = None
		self.signal = None
		self.octave = None
		self.channels = None
		self.frequency = None
		self.no_samples = None
		self.sample_rate = None
		self.sample_width = None

	def read(self, filename):
		''' Read and prepare the audio file. '''

		# try to extract attributes from wav file.
		try:
			wav = wave.open(filename, 'r')
			frames = wav.getnframes()
			self.sample_rate = wav.getframerate()
			self.channels = wav.getnchannels()
			self.sample_width = wav.getsampwidth()
			self.signal = wav.readframes(frames)
			self.no_samples, remainder = divmod(len(self.signal), self.sample_width * self.channels)

			# if there are more than two channels, raise exception.
			if( self.channels > 2 ):
				raise ValueError
				sys.exit(1)

			# if there are two channels, average them.
			elif( self.channels == 2 ):
				actual = ''
				for (sample1, sample2) in zip(self.signal[0::2], self.signal[1::2]):
					actual += hex((ord(sample1) + ord(sample2)) / 2)[2:].zfill(2).decode('hex')
				self.signal = actual
				self.no_samples /= 2

			# create numpy array to represent signal string as appropriate data type
			# according to the sample width.
			if( self.sample_width > 4 ):
				raise wave.Error 
				sys.exit(1)

			if( self.sample_width == 3 ):
				array = numpy.empty((self.no_samples, self.channels, 4), dtype = numpy.uint8)
				raw_bytes = numpy.fromstring(self.signal, dtype = numpy.uint8)
				array[:, :, :self.sample_width] = raw_bytes.reshape(-1, self.channels, self.sample_width)
				array[:, :, self.sample_width:] = (array[:, :, self.sample_width - 1:self.sample_width] >> 7) * 255
				self.signal = array.view('<i4').reshape(array.shape[:-1])
				self.signal = self.signal.reshape(-1)

			else:
				if( self.sample_width == 1 ):
					dt_char = 'u'
				else:
					dt_char = 'i'
				array = numpy.fromstring(self.signal, dtype = '<%s%d' % (dt_char, self.sample_width))
				self.signal = array.reshape(-1)

			wav.close()

		except EOFError:
			raise EOFError
			sys.exit(1)

		except IOError:
			raise IOError
			sys.exit(1)

		except wave.Error:
			raise wave.Error
			sys.exit(1)

	def getFrequency(self, signal, sample_rate):
		''' Determine the frequency of the signal. '''

		# correct the signal.
		signal = scipy.signal.fftconvolve(signal, signal[::-1], mode='full')
		signal = signal[len(signal)/2:]

		# find the first minimum point in the signal.
		difference = numpy.diff(signal)
		start = matplotlib.mlab.find(difference > 0)[0]
    
		# find the peak from that position.
		peak = numpy.argmax(signal[start:]) + start

		# calculate the period using parabolic interpolation.
		period = 1/2.0 * (signal[peak-1] - signal[peak+1]) / (signal[peak-1] - 2 * signal[peak] + signal[peak+1]) + peak
    
		return (sample_rate / period)

	def getNote(self, frequency):
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
	notepicker = NotePicker()
	notepicker.read('../Music/c1.wav')
'''	audio = []
	for index in range(1, len(sys.argv)):
		audio.append(str(sys.argv[index]))
	for filename in audio:
		start_time = time.time()
		signal, sample_rate = read(filename)
		freq = findFrequency(signal, sample_rate)
		print '******************************'
		print 'Number of Samples: %i' % len(signal)
		print 'Sample rate: %i' % sample_rate
		print 'Frequency: %.3f' % freq
		print 'Note: %s' % recognize(freq)
		print 'Time elapsed: %.3f s' % (time.time() - start_time)
'''
