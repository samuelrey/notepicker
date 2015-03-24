from scikits.audiolab import wavread, Sndfile
from numpy import argmax, diff, linspace, array
from matplotlib.pyplot import plot, show
from matplotlib.mlab import find
from scipy.signal import fftconvolve
from time import time
from sys import argv, exit
from traceback import format_exc

OCTAVES = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034.0, 4068.0, 7902.0]
BASE_FR = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
BASE_NO = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']

def read(filename):
	''' Read the audio file and return the raw signal, sample rate and number of channels. '''
	
	# try to extract signal, sample rate and number of channels.
	# exit if cannot open file.
	try:
		signal, sample_rate, encoding = wavread(filename)
		channels = Sndfile(filename, 'r').channels
		
	# if there are more than one channels, just use the first.
		if channels > 1:
			actual = []
			for sample in signal:
				actual.append(sample[0])
			signal = array(actual)
	except IOError:
		print 'Error: Cannot open %s' % filename
		print format_exc()
		exit(0)
		
	return signal, sample_rate
	
def graph(signal, sample_rate):
	''' Plot the signal. '''
	
	# plot with respect to time.
#	Time = linspace(0, len(signal) / sample_rate, num = len(signal))
#	plot(Time, signal)

	# plot with respect to the number of samples.
	plot(signal)
	show()

def autocorrelate(signal):
	''' Autocorrelate the signal. '''

	# create third signal using Fast Fourier Transform 
	# and convolution of the signal and itself.
	# remove the negative lag.
	auto = fftconvolve(signal, signal[::-1], mode='full')
	auto = auto[len(auto)/2:]
	
	return auto

def findFrequency(signal, sample_rate):
	''' Determine the frequency of the signal. '''

	# find the first minimum point in the signal.
	difference = diff(signal)
	start = find(difference > 0)[0]
    
    # find the peak from that position.
    # calculate the period using quadratic interpolation.
	peak = argmax(signal[start:]) + start
	period = 1/2.0 * (signal[peak-1] - signal[peak+1]) / (signal[peak-1] - 2 * signal[peak] + signal[peak+1]) + peak
    
	return (sample_rate / period), start, period

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
			
	return note, octave

if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		audio = []
		for index in range(1, len(argv)):
			audio.append(str(argv[index]))
	
		for filename in audio:
			start_time = time()
			signal, sample_rate = read(filename)
			auto = autocorrelate(signal)
			freq, start, period = findFrequency(auto, sample_rate)
			print '******************************'
			print 'Frequency: %.3f' % freq
			print 'Note: %s%i' % recognize(freq)
			print 'Time elapsed: %.3f s' % (time() - start_time)
