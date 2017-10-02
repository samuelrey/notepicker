import numpy
import wave

class track:
    def __init__(self):
        self.signal = None
        self.sample_rate = None

    def read(self, filename):
        ''' Read and prepare the audio file. '''

        # try to extract attributes from wav file.
        wav = wave.open(filename, 'r')

        # read signal
        frames = wav.getnframes()
        self.signal = wav.readframes(frames)
        self.sample_rate = wav.getframerate()

        # if there are two channels, average them.
        channels = wav.getnchannels()
        if channels == 2:
            combined = ''
            indices = numpy.arange(len(self.signal))
            for index in indices[0::4]:
                first = hex((ord(self.signal[index]) + ord(self.signal[index + 2])) / 2)[2:].zfill(2)
                second = hex((ord(self.signal[index + 1]) + ord(self.signal[index + 3])) / 2)[2:].zfill(2)
                combined = first.decode('hex') + second.decode('hex')
            self.signal = combined
            self.signal = numpy.fromstring(self.signal, dtype='<i2')

        wav.close()