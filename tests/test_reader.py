import unittest
from rnnlm.models.lstm_fast import reader


class TestReader(unittest.TestCase):

    def test_read_n_shifted_words(self):
        read_n = reader._read_n_shifted_words
        self.assertEqual(list(read_n([], 2)), [])
        self.assertEqual(list(read_n(['1', '2', '3', '4'], 2)), [['1', '2'], ['2', '3'], ['3', '4'], ['4']])
        self.assertEqual(list(read_n(['2'], 1)), [['2']])
        self.assertEqual(list(read_n(['1'], 2)), [['1']])
        self.assertEqual(list(read_n(['1', '2'], 0)), [['1', '2']])
