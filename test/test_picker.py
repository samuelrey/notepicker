# Filename: read.py
#
# Summary: unit tests read method
#
# Author: Samuel Villavicencio
#
# Last Updated: Oct 09 2015

import sys
import unittest
import wave

sys.path.append('/home/psycho/Projects/Note_Picker/Source')
import _write
import picker


class ReadTest(unittest.TestCase):
    def testFileDoesNotExist(self):
        np = picker.Picker()
        files = ['', 'nonexistent']

        for file in files:
            try:
                np.read(file)
            except IOError:
                pass
            else:
                self.fail('Expected error reading nonexistent file - ' + file)

    def testUnsupportedFile(self):
        np = notepicker.NotePicker()
        files = ['read.py', '../README.md']

        for file in files:
            try:
                np.read(file)
            except wave.Error:
                pass
            else:
                self.fail('Expected error reading unsupported file - ' + file)

    def testSupportedChannels(self):
        file = 'test.wav'
        np = notepicker.NotePicker()

        try:
            for channels in range(1, 2):
                _write.generateNote(channels, 1, 44100, 1, 440)
                np.read(file)

                self.assertEqual(np.channels, channels)
                self.assertEqual(np.sample_width, 1)
                self.assertEqual(np.sample_rate, 44100)

                self.assertIsNone(np.note)
                self.assertIsNone(np.octave)
                self.assertIsNone(np.frequency)

                self.assertIsNotNone(np.signal)
                self.assertIsNotNone(np.no_samples)

        except:
            self.fail('Error reading file with supported channels.')
        finally:
            _write.removeNote()

    def testUnsupportedChannels(self):
        file = 'test.wav'
        np = notepicker.NotePicker()

        try:
            for channels in [3, sys.maxint]:
                _write.generateNote(channels, 1, 44100, 1, 440)
                np.read(file)
        except:
            pass
        else:
            self.fail('Expected error reading unsupported channels.')
        finally:
            _write.removeNote()

    def testSupportedSampleWidth(self):
        file = 'test.wav'
        np = notepicker.NotePicker()

        try:
            for sample_width in range(1, 5):
                _write.generateNote(1, sample_width, 44100, 1, 440)
                np.read(file)
                self.assertEqual(np.channels, 1)
                self.assertEqual(np.sample_width, sample_width)
                self.assertEqual(np.sample_rate, 44100)

                self.assertIsNone(np.note)
                self.assertIsNone(np.octave)
                self.assertIsNone(np.frequency)

                self.assertIsNotNone(np.signal)
                self.assertIsNotNone(np.no_samples)

        except:
            self.fail('Error reading supported sample width.')
        finally:
            _write.removeNote()

    def testSupportedSampleRate(self):
        file = 'test.wav'
        np = notepicker.NotePicker()

        try:
            for sample_rate in [8000, 11025, 22050, 32000, 44100, 48000, 64000, 88200, 96000]:
                _write.generateNote(1, 2, sample_rate, 1, 440)
                np.read(file)

                self.assertEqual(np.channels, 1)
                self.assertEqual(np.sample_width, 2)
                self.assertEqual(np.sample_rate, sample_rate)

                self.assertIsNone(np.note)
                self.assertIsNone(np.octave)
                self.assertIsNone(np.frequency)

                self.assertIsNotNone(np.signal)
                self.assertIsNotNone(np.no_samples)
        except:
            self.fail('Error reading supported sample rate.')
        finally:
            _write.removeNote()


if __name__ == '__main__':
    unittest.main()
