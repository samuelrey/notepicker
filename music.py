from frequency import read, autocorrelate, findFrequency, recognize
from identify import findPeaks, findNotes
from traceback import format_exc
from time import time
from sys import argv

def musicalNotes(signal, sample_rate, notes):
	music = []
	for note in notes:
		try:
			auto = autocorrelate(signal[note[0]:note[1]])
			freq = findFrequency(auto, sample_rate)
			music.append(recognize(freq))
		except UnboundLocalError:
			print 'Error: Cannot identify note at sample %i' % note[0]
			print format_exc()
			continue
	return music
			
if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		start_time = time()
		signal, sample_rate = read(argv[1])
		peaks = findPeaks(signal)
		notes = findNotes(signal, peaks)
		music = musicalNotes(signal, sample_rate, notes)
