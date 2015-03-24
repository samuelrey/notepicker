from numpy import greater, argmax, size, mean
from scipy.signal import argrelextrema
from frequency import read, graph
from time import time
from sys import argv

# Values *adjusted* for the first 3 seconds of 
# Seven Nation Army by Jack White.
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
THRESHOLD=.08
NOTE=10
BREAK=22

def findPeaks(signal):
	''' Find all of the peaks in the signal. '''
	
	peaks = argrelextrema(signal, greater)[0]

	return peaks
	
def findNotes(signal, peaks):
	''' Estimates the number of notes in the signal. '''
	
	# no_greater refers to the number of peaks above 
	# the threshold.
	# no_less refers to the number of consecutive
	# peaks below the threshold.
	# unique marks a potential note for the storage
	# of the indices where it starts and ends.
	no_greater = 0
	no_less = 0
	unique = True
	notes = []

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
	return notes

if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		audio = []
		for index in range(1, len(argv)):
			audio.append(str(argv[index]))
	
		for filename in audio:
			signal, sample_rate = read(filename)
			start_time = time()
			peaks = findPeaks(signal)
			notes = findNotes(signal, peaks)
			print '******************************'
			print 'Number of notes: %i' % len(notes)
			print 'Time elapsed: %.3f s' % (time() - start_time)
			for note in notes:
				graph(signal[note[0]:note[1]], sample_rate)
