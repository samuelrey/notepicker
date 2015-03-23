from numpy import argmax
from frequency import read
from sys import argv

# Adjust values.
VOLUME	# Threshold
END
NOTE
BREAK

signal, sample_rate, channels = read(argv[1])

def findNotes(signal):

	index = argmax(signal)
	peak = signal[index]
	no_greater = 0
	no_less = 0
	notes = []

	while( len(signal) - index < END ):
		if( peak > VOLUME ):
			start = index
			no_greater = no_greater + 1
			while( no_less < BREAK ):
				index = argmax(signal[index:])
				peak = signal[index]
				if( peak < VOLUME ):
					no_less = no_less + 1
				else:
					no_greater = no_greater + 1
					no_less = 0
			end = index
			if( no_greater > NOTE ):
				note = (start, end)
				notes.append(note)
		index = argmax(signal[index:])
		peak = signal[index]
