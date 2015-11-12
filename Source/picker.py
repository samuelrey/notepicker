# Filename: notepicker.py
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

class Picker():

	def __init__(self):
		self.notes = ()			# tuple of Note objects
		self.signal = numpy.empty(0)	# ndarray of amplitudes
		self.channels = 0
		self.frequency = 0.0
		self.no_samples = 0
		self.sample_rate = 0

	def read(self, filename):
		''' Read and prepare the audio file. '''

		# try to extract attributes from wav file.
		try:
			wav = wave.open(filename, 'r')
			frames = wav.getnframes()
			sample_width = wav.getsampwidth()
			self.sample_rate = wav.getframerate()
			self.channels = wav.getnchannels()
			self.signal = wav.readframes(frames)

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

			self.signal = numpy.fromstring(self.signal, dtype = '<i2')
			self.no_samples = len(self.signal)

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

	# TODO
	# Values must be adjusted for different songs
	# THRESHOLD is a value that represents a
	# minimum value in volume of the signal to
	# start determining if there is an audible
	# note.
	# NOTE is the minimum number of peaks above
	# the threshold to consider the part of the
	# signal an actual note.
	# BREAK is the minimum number of consecutive
	# peaks below the threshold to signify the
	# end of a possible note.

	def findNotes(self, signal):
		''' Estimates the number of notes in the signal. '''
		THRESHOLD=.45
		NOTE=50
		BREAK=50

		# no_greater refers to the number of peaks above 
		# the threshold.
		# no_less refers to the number of consecutive
		# peaks below the threshold.
		# unique marks a potential note for the storage
		# of the indices where it starts and ends.
		start = 0
		end = 0
		no_greater = 0
		no_less = 0
		unique = True
		notes = []
		peaks = scipy.signal.argrelextrema(signal, numpy.greater)[0]

		# for every peak, check where it lies with 
		# respect to the threshold.
		for peak in peaks:

			# if it is above, check if the note is
			# unique, increment the no_greater and
			# reset no_less.
			if( signal[peak] > THRESHOLD ):

				if( unique ):
					unique = False
					start = peak

				else:
					end = peak
				no_greater = no_greater + 1
				no_less = 0
	
			# otherwise, increment the no_less.
			else:
				no_less = no_less + 1

			# if no_less is greater than BREAK,
			# check if no_greater is greater than
			# NOTE, append the note to the list if
			# appropriate, and reset the rest of 
			# the values.
			if( no_less > BREAK ):
	
				if( no_greater > NOTE ):
					note = (start, end)
					notes.append(note)
				no_greater = 0
				no_less = 0
				unique = True
		if( no_greater > NOTE ):
			note = (start, end)
			notes.append(note)

		return notes
	'''

'''
if __name__ == '__main__':
	notepicker = NotePicker()
	notepicker.read('../Music/c1.wav')
	notepicker.getFrequency()
	print notepicker.frequency
	audio = []
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
