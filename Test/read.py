''' Unit Tests for read method. '''
import sys
import wave
import unittest
sys.path.append('/home/psycho/Projects/Note_Picker/Source')
import frequency

class ReadTest(unittest.TestCase):
	def testFileDoesNotExist(self):
		nonexistent_file = ['', 'nonexistent']

		for file in nonexistent_file:
			try:
				signal, sample_rate = frequency.read(file)
			except IOError:
				pass
			else:
				self.fail('Expected error reading nonexistent file - ' + file)

	def testUnsupportedFile(self):
		unsupported_file = '../README.md'
		
		try:
			signal, sample_rate = frequency.read(unsupported_file)
		except wave.Error:
			pass
		else:
			self.fail('Expected error reading unsupported file - ' + unsupported_file)

	def testSupportedFile(self):
		supported_file = ['../Music/c1.wav'] #, '../Music/Mochi Pug.wav']

		for file in supported_file:
			try:
				signal, sample_rate = frequency.read(file)
			except:
				self.fail('Error reading file - ' + file)

	def testSameType(self):
		file_one = '../Music/c1.wav'
		file_two = '../Music/e3.wav' #'../Music/Mochi Pug.wav'
		
		signal_one, rate_one = frequency.read(file_one)
		signal_two, rate_two = frequency.read(file_two)

		self.assertEqual(type(signal_one), type(signal_two))
		self.assertEqual(type(rate_one), type(rate_two))

if __name__ == '__main__':
	unittest.main()
