# Filename: _write.py
#
# Summary: writes single note wav files for testing
#
# Author: Samuel Villavicencio
#
# Last Updated: Oct 09 2015

import os
import math
import wave
import struct

def generateNote(channels, sample_width, sample_rate, length, frequency):
	''' Write metadata and signal to audio file. '''

	signal = []

	output = wave.open('test.wav', 'w')
	output.setparams((channels, sample_width, sample_rate, 0, 'NONE', 'not compressed'))

	# calculate every sample to fit a sinusoidal plot with a given frequency.
	for i in range(length * sample_rate):
		value = math.sin(2 * math.pi * frequency * (i / float(sample_rate)))
		packed = struct.pack('h', int(value * 4000.0 / 2))
		for j in range(channels):
			signal.append(packed)

	signal = ''.join(signal)
	output.writeframes(signal)
	output.close()

def removeNote():
	''' Remove audio file. '''

	os.remove('test.wav')
