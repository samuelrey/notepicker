from frequency import read, graph

if __name__ == '__main__':
	if(len(argv) < 2):
		print 'Usage: python %s <filename>' % argv[0]
		exit(1)
	else:
		filename = argv[1]
		signal, sample_rate = read(filename)
		print "Number of samples %i" % len(signal)
		graph(signal, sample_rate)
