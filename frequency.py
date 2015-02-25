from scikits.audiolab import wavread
from numpy import argmax, diff, linspace
from matplotlib.mlab import find
from scipy.signal import fftconvolve
from time import time

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
    
def test():
	
	audio = ['c1.wav', 'c2.wav', 'c3.wav', 'e1.wav', 'e2.wav', 'e3.wav', 'g#1.wav', 'g#2.wav', 'g#3.wav']
	
	for filename in audio:
		signal, sample_rate, encoding = wavread(filename)
		
		print '*******************************************'
		print 'Reading: ' + filename
		start_time = time()
		print '%f Hz' % autocorr(signal, sample_rate)
		print 'Time elapsed: %.3f s\n' % (time() - start_time)
		
		
test()
