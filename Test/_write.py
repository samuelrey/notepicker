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
import numpy
import struct
import random

filename = 'test.wav'

def note(channels, sample_width, sample_rate, length, frequency):
	''' Write metadata and signal to audio file. '''

	signal = []

	output = wave.open(filename, 'w')
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

def uniform(amplitude, length):
	''' Write a single amplitude to audio file. '''

	signal = []

	output = wave.open(filename, 'w')
	output.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))

	for i in range(length * 44100):
		packed = struct.pack('h', int(amplitude * 4000.0 / 2))
		signal.append(packed)

	signal = ''.join(signal)
	output.writeframes(signal)
	output.close()

def rand(length):
	''' Write random noise to audio file. '''

	signal = []

	output = wave.open(filename, 'w')
	output.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))

	for i in range(length * 44100):
		packed = struct.pack('h', random.randint(-32767, 32767))
		signal.append(packed)

	signal = ''.join(signal)
	output.writeframes(signal)
	output.close()

def read():
	''' Generic method to read fixed data. '''

	wav = wave.open(filename, 'r')
	frames = wav.getnframes()
	sample_width = wav.getsampwidth()
	sample_rate = wav.getframerate()
	channels = wav.getnchannels()
	signal = wav.readframes(frames)
	signal = numpy.fromstring(signal, dtype = '<i2')
	no_samples = len(signal)
	
	return signal, sample_rate

def clean():
	''' Remove audio file. '''

	os.remove(filename)
