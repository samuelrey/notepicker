# Filename: getFrequency.py
#
# Summary: unit tests getFrequency method.
#
# Author: Samuel Villavicencio
#
# Last Updated: Oct 09 2015

import sys
import unittest
sys.path.append('/home/psycho/Projects/Note_Picker/Source')
import _write
import notepicker

class GetFrequencyTest(unittest.TestCase):
	def testEdgeFrequencies(self):
		file = 'test.wav'
		np = notepicker.NotePicker()

		try:
			for frequency in [20, 4000]:
				_write.generateNote(1, 2, 44100, 1, frequency)
				np.read(file)
				np.getFrequency()

				self.assertIsNotNone(np.frequency)
				self.assertAlmostEqual(np.frequency, frequency, places = 0)
		except:
			self.fail('Error calculating frequency.')
		finally:
			_write.removeNote()


if __name__ == '__main__':
	unittest.main()
