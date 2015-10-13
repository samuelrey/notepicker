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
			if( self.channels == 2 ):
				actual = ''
				indices = numpy.arange(len(self.signal))
				for index in indices[0::4]:
					first = hex((ord(self.signal[index]) + ord(self.signal[index + 2])) / 2)[2:].zfill(2)
					second = hex((ord(self.signal[index + 1]) + ord(self.signal[index + 3])) / 2)[2:].zfill(2)
					actual = actual + first.decode('hex')
					actual = actual + second.decode('hex')

				self.signal = actual

			# create numpy array to represent signal string as appropriate data type
			# according to the sample width.
			if( self.sample_width > 4 ):
				raise wave.Error 
				sys.exit(1)

			self.signal = numpy.fromstring(self.signal, dtype = '<i2')
				
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

	def getFrequency(self):
		''' Determine the frequency of the signal. '''

		try:
			# correct the signal.
			auto = scipy.signal.fftconvolve(self.signal, self.signal[::-1], mode='full')
			auto = auto[len(auto)/2:]

			# find the first minimum point in the signal.
			difference = numpy.diff(auto)
			start = matplotlib.mlab.find(difference > 0)[0]

			# find the peak from that position.
			peak = numpy.argmax(auto[start:]) + start
			# calculate the period using parabolic interpolation.
			period = 1/2.0 * (auto[peak-1] - auto[peak+1]) / (auto[peak-1] - 2 * auto[peak] + auto[peak+1]) + peak
			self.frequency = self.sample_rate / period
		except:
			print traceback.format_exc()

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
	notepicker.getFrequency()
	print notepicker.frequency
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
