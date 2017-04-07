# Filename: frequency.py
#
# Summary: plots wav files
#
# Author: Samuel Villavicencio
# 
# Last Updated: Oct 07 2015

import matplotlib.pyplot  # plot show


def graph(signal, sample_rate):
    ''' Plot the signal. '''

    # plot with respect to time.
    #	Time = numpy.linspace(0, len(signal) / sample_rate, num = len(signal))
    #	matplotlib.pyplot.plot(Time, signal)

    # plot with respect to the number of samples.
    matplotlib.pyplot.plot(signal)
    matplotlib.pyplot.show()
