# Filename: getFrequency.py
#
# Summary: unit tests getFrequency method.
#
# Author: Samuel Villavicencio
#
# Last Updated: Oct 09 2015

import sys
import unittest
import traceback
sys.path.append('/home/psycho/Projects/Note_Picker/Source')
import _write
import note

class GetFrequencyTest(unittest.TestCase):

	def testEmptySignal(self):
		n = note.Note()
		_write.note(1, 2, 44100, 0, 440)

		try:
			signal, sample_rate = _write.read()
			n.getFrequency(signal, sample_rate)
		except:
			_write.clean()
			pass
		else:
			_write.clean()
			self.fail()

	def testMaxFrequency(self):
		# values between sample_rate * n and sample_rate * (n + 1) are mistakenly valid. 
		n = note.Note()
		_write.note(1, 2, 44100, 1, 22049)							
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))

			self.assertAlmostEqual(22049, n.getFrequency(signal, sample_rate), 1)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testMinFrequency(self):
		n = note.Note()
		_write.note(1, 2, 44100, 1, 1)
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))

			self.assertAlmostEqual(1, n.getFrequency(signal, sample_rate), 1)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testPositiveUniformSignal(self):
		n = note.Note()
		_write.uniform(1, 1)
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))
			n.getFrequency(signal, sample_rate)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testZeroUniformSignal(self):
		n = note.Note()
		_write.uniform(0, 1)
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))
			n.getFrequency(signal, sample_rate)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testNegativeUniformSignal(self):
		n = note.Note()
		_write.uniform(-1, 1)
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))
			n.getFrequency(signal, sample_rate)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testRandomSignal(self):
		n = note.Note()
		_write.rand(1)
		try:
			signal, sample_rate = _write.read()
			n.setTotalLength(signal)
			n.setStart(0)
			n.setLength(len(signal))
			n.getFrequency(signal, sample_rate)
		except:
			_write.clean()
			self.fail( traceback.format_exc() )
		else:
			_write.clean()
			pass

	def testAccuracy(self):
		try:
			for frequency in range(40, 22040, 2000):
				n = note.Note()
				_write.note(1, 2, 44100, 1, frequency)
				signal, sample_rate = _write.read()
				n.setTotalLength(signal)
				n.setStart(0)
				n.setLength(len(signal))
				calculated = n.getFrequency(signal, sample_rate)
				_write.clean()
				self.assertAlmostEqual(frequency, calculated, 0)
		except:
			self.fail( traceback.format_exc() )
		else:
			pass

class GetNotationTest(unittest.TestCase):
	
	def testNoMatchingFrequency(self):
		for frequency in [7680.5]:	# find more frequencies
			n = note.Note()
			_write.note(1, 2, 44100, 1, frequency)
			try:
				signal, sample_rate = _write.read()
				n.setTotalLength(signal)
				n.setStart(0)
				n.setLength(len(signal))

				frequency = n.getFrequency(signal, sample_rate)
				n.getNotation(frequency)
			except:
				_write.clean()
				pass
			else:
				_write.clean()
				self.fail( traceback.format_exc() )

	def testNoMatchingOctave(self):
		for frequency in [8000.0]:
			n = note.Note()
			_write.note(1, 2, 44100, 1, frequency)
			try:
				signal, sample_rate = _write.read()
				n.setTotalLength(signal)
				n.setStart(0)
				n.setLength(len(signal))

				frequency = n.getFrequency(signal, sample_rate)
				n.getNotation(frequency)
			except:
				_write.clean()
				pass
			else:
				_write.clean()
				self.fail( traceback.format_exc() )

if __name__ == '__main__':
	unittest.main()
