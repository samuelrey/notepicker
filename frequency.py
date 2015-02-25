from scikits.audiolab import wavread
from numpy import argmax, diff, linspace
from matplotlib.mlab import find
from scipy.signal import fftconvolve
from time import time

octaves = [31.7, 63.5, 127.1, 254.2, 508.6, 1017.4, 2034, 4068, 7902]
base_freqs = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
base_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def frequency(signal, sample_rate):
    
    # create third signal using Fourier Transform and convolution of the signal and reverse
    auto = fftconvolve(signal, signal[::-1], mode='full')
    auto = auto[len(auto)/2:]
    
    # get first positive low point excluding 0 lag
    d = diff(auto)
    start = find(d > 0)[0]
    
    # find the peak from the start of the signal
    # find the distance between peaks
    peak = argmax(auto[start:]) + start
    px = 1/2.0 * (auto[peak-1] - auto[peak+1]) / (auto[peak-1] - 2 * auto[peak] + auto[peak+1]) + peak
    
    # return the frequency
    return sample_rate / px
    
def recognition(frequency):
	for index in range(9):
		if(frequency < octaves[index]):
			octave = index
			break
	
	adj_freq = adjust(frequency, octave)
	
	for index in range(12):
		if(abs(base_freqs[index] - adj_freq) < .6):
			note = base_notes[index]
			break
			
	return note, octave
	
def adjust(frequency, factor):
	return frequency / (2 ** factor)
	
def test():
	audio = ['a1.wav', 'a2.wav', 'a3.wav', 'a4.wav', 'c1.wav', 'c2.wav', 'c3.wav', 'c4.wav', 'c5.wav', 'c6.wav', 'e1.wav', 'e2.wav', 'e3.wav', 'e4.wav', 'e5.wav', 'g#1.wav', 'g#2.wav', 'g#3.wav', 'g#4.wav', 'g#5.wav']
	
	for filename in audio:
		signal, sample_rate, encoding = wavread(filename)
		
		print '*******************************************'
		# print 'Reading: ' + filename
		start_time = time()
		freq = frequency(signal, sample_rate)
		print '%s %i' % recognition(freq)
		print 'Time elapsed: %.3f s\n' % (time() - start_time)
		
test()
		
'''
TEST FREQUENCY
def test():
	
	audio = ['c1.wav', 'c2.wav', 'c3.wav', 'e1.wav', 'e2.wav', 'e3.wav', 'g#1.wav', 'g#2.wav', 'g#3.wav']
	
	for filename in audio:
		signal, sample_rate, encoding = wavread(filename)
		
		print '*******************************************'
		print 'Reading: ' + filename
		start_time = time()
		print '%f Hz' % frequency(signal, sample_rate)
		print 'Time elapsed: %.3f s\n' % (time() - start_time)
		
		
test()
'''
