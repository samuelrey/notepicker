# Filename: note.py
#
# Summary: defines note class.
#
# Author: Samuel Villavicencio
#
# Last Updated Oct 17 2015

import numpy			#
import numpy.fft		#
import traceback		#
import scipy.signal		#
import matplotlib.mlab		#

class Note():

	def __init__( self, start = 0, length = 0, signal = numpy.empty(0) ):
		self.frequency = 0.0
		self.notation = ""
		self.start = start
		self.length = length
		self.total_length = len(signal)

	def getFrequency(self, signal, sample_rate):
		''' Determine the frequency of the signal. '''

		# return the value if it has already been calculated.
		if self.frequency != 0.0:
			return self.frequency

		if self.total_length != len(signal):
			raise ValueError
		
		try:
			numpy.seterr(divide='ignore', invalid='ignore')
			windowed = signal + scipy.signal.blackmanharris(len(signal))
			f = numpy.fft.rfft(windowed)
			i = numpy.argmax(abs(f))
			true_i = 1/2.0 * (numpy.log(abs(f))[i-1] - numpy.log(abs(f))[i+1]) / (numpy.log(abs(f))[i-1] - 2 * numpy.log(abs(f))[i] + numpy.log(abs(f))[i+1]) + i
			self.frequency = sample_rate * true_i / len(windowed)
			return self.frequency
		
		except ValueError:
			raise ValueError
		except IndexError:
			raise IndexError
		except TypeError:
			raise TypeError

	def getNotation(self, frequency):
		''' Match the frequency to the musical note. '''

		# return the value if it has already been calculated.
		if len(self.notation) != 0:
			return self.notation

		# octaves represents the frequency bounds of every octave
		# base_fr represents the individual frequencies in the 0th octave
		# base_no represents the musical notation of the base frequencies
		octaves = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034.0, 4068.0, 7902.0]
		base_no = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']
		base_fr = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]


		try:
			# get the octave of the frequency.
			for index, value in enumerate(octaves):
				if(frequency < value):
					octave = index
					break

			# adjust the frequency.
			adjusted = frequency / (2 ** octave)

			# get the letter note of the frequency.
			for index in range(12):
				if(abs(base_fr[index] - adjusted) < .6):
					note = base_no[index]
					break

			self.notation = note + str(octave)

			return self.notation

		except UnboundLocalError:
			raise UnboundLocalError

	def setTotalLength(self, signal):
		''' Set the total length of the signal. '''

		try:
			self.total_length = len(signal)
		# catch all exceptions.
		except:
			print traceback.format_exc()

	def setStart(self, start):
		''' Set the starting index of the note. '''

		try:
			if start >= self.total_length:
				raise ValueError

			elif start + self.length > self.total_length:
				raise ValueError

			else:
				self.start = start
		# catch all exceptions.
		except:
			print traceback.format_exc()

	def setLength(self, length):
		''' Set the length of the note. '''

		try:
			if length > self.total_length:
				raise ValueError

			elif self.start + length > self.total_length:
				raise ValueError

			else:
				self.length = length
		# catch all exceptions.
		except:
			print traceback.format_exc()
