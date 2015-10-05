from frequency import read, graph
from sys import argv

if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		filename = argv[1]
		signal, sample_rate = read(filename)
		print "Number of samples %i" % len(signal)
		graph(signal[:len(signal) / 2], sample_rate)
		graph(signal[len(signal) / 2:], sample_rate)
