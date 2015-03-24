from frequency import read, autocorrelate, findFrequency, recognize
from identify import findPeaks, findNotes
from time import time
from sys import argv

if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		start_time = time()
		signal, sample_rate = read(argv[1])
		peaks = findPeaks(signal)
		notes = findNotes(signal, peaks)
		for note in notes:
			auto = autocorrelate(signal[note[0]:note[1]])
			freq, start, period = findFrequency(auto, sample_rate)
			print '******************************'
			print 'Frequency: %.3f' % freq
			print 'Note: %s%i' % recognize(freq)
			print 'Time elapsed: %.3f s' % (time() - start_time)
