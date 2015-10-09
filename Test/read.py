# Filename: read.py
#
# Summary: unit tests read method
#
# Author: Samuel Villavicencio
#
# Last Updated: Oct 09 2015

import os
import sys
import math
import wave
import struct
import unittest
sys.path.append('/home/psycho/Projects/Note_Picker/Source')
from notepicker import NotePicker

def generateNote(channels, sample_width, sample_rate, length, frequency):
	signal = []

	output = wave.open('test.wav', 'w')
	output.setparams((channels, sample_width, sample_rate, 0, 'NONE', 'not compressed'))

	for i in range(length * sample_rate):
		value = math.sin(2 * math.pi * frequency * (i / float(sample_rate)))
		packed = struct.pack('h', int(value * 2000.0 / 2))
		signal.append(packed)

	signal = ''.join(signal)
	output.writeframes(signal)
	output.close()

def removeNote():
	os.remove('test.wav')

class ReadTest(unittest.TestCase):
	def testFileDoesNotExist(self):
		notepicker = NotePicker()
		files = ['', 'nonexistent']

		for file in files:
			try:
				notepicker.read(file)
			except IOError:
				pass
			else:
				self.fail('Expected error reading nonexistent file - ' + file)

	def testUnsupportedFile(self):
		notepicker = NotePicker()
		files = ['read.py', '../README.md']
		
		for file in files:
			try:
				notepicker.read(file)
			except wave.Error:
				pass
			else:
				self.fail('Expected error reading unsupported file - ' + file)

	def testSupportedChannels(self):
		file = 'test.wav'
		notepicker = NotePicker()

		try:
			for channels in range(1, 2):
				generateNote(channels, 1, 44100, 1, 440)
				notepicker.read(file)

				self.assertEqual(notepicker.channels, channels)
				self.assertEqual(notepicker.sample_width, 1)
				self.assertEqual(notepicker.sample_rate, 44100)

				self.assertIsNone(notepicker.note)
				self.assertIsNone(notepicker.octave)
				self.assertIsNone(notepicker.frequency)

				self.assertIsNotNone(notepicker.signal)
				self.assertIsNotNone(notepicker.no_samples)

		except:
			self.fail('Error reading file with supported channels.')
		finally:
			removeNote()

	def testUnsupportedChannels(self):
		file = 'test.wav'
		notepicker = NotePicker()

		try:
			for channels in [3, sys.maxint]:
				generateNote(channels, 1, 44100, 1, 440)
				notepicker.read(file)
		except ValueError:
			pass
		else:
			self.fail('Expected error reading unsupported channels.')
		finally:
			removeNote()

	def testSupportedSampleWidth(self):
		file = 'test.wav'
		notepicker = NotePicker()

		try:
			for sample_width in range(1, 4):
				generateNote(1, sample_width, 44100, 1, 440)
				notepicker.read(file)

				self.assertEqual(notepicker.channels, 1)
				self.assertEqual(notepicker.sample_width, sample_width)
				self.assertEqual(notepicker.sample_rate, 44100)

				self.assertIsNone(notepicker.note)
				self.assertIsNone(notepicker.octave)
				self.assertIsNone(notepicker.frequency)

				self.assertIsNotNone(notepicker.signal)
				self.assertIsNotNone(notepicker.no_samples)
		except:
			self.fail('Error reading supported sample width.')
		finally:
			removeNote()

	def testSupportedSampleRate(self):
		file = 'test.wav'
		notepicker = NotePicker()

		try:
			for sample_rate in [8000, 11025, 22050, 32000, 44100, 48000, 64000, 88200, 96000]:
				generateNote(1, 2, sample_rate, 1, 440)
				notepicker.read(file)

				self.assertEqual(notepicker.channels, 1)
                                self.assertEqual(notepicker.sample_width, 2)
                                self.assertEqual(notepicker.sample_rate, sample_rate)

                                self.assertIsNone(notepicker.note)
                                self.assertIsNone(notepicker.octave)
                                self.assertIsNone(notepicker.frequency)

                                self.assertIsNotNone(notepicker.signal)
                                self.assertIsNotNone(notepicker.no_samples)
		except:
			self.fail('Error reading supported sample rate.')
		finally:
			removeNote()

if __name__ == '__main__':
	unittest.main()
