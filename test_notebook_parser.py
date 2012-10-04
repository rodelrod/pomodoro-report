#!/usr/bin/env python
import unittest
from notebook_parser import *
import os
import errno
from datetime import datetime


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: 
        if exc.errno == errno.EEXIST:
            pass
        else: 
            raise


class TestParser(unittest.TestCase):

    """Tests the RedNotebook monthly files parser."""

    def setUp(self):
        self.nb_path = '/tmp/test_pomodoro_report'
        mkdir_p(self.nb_path)
        f = open(os.path.join(self.nb_path, '2012-10.txt'), 'w')
        f.write(
            "21: {text: '1/1 fix import sewan\n"
            "    2/2 check fidelidade, delete 0836\n"
            "    0/1 org desk'}\n"
            "25:\n" 
            "    Cat3: {Some other shit: null}\n"
            "    text: '1/1 fix import sewan\n"
            "          2/2 check fidelidade, delete 0836\n"
            "          0/1 org desk'\n"
            "27:\n" 
            "    Cat1: {Some shit: null}\n"
            "    text: '1/1 fix import sewan\n"
            "          2/2 check fidelidade, delete 0836\n"
            "          0/1 report incongruencias sewan pdf/cdr\n"
            "          1/1 fix b''illing db and run\n"
            "          0/2 guide entretien prestataire\n"
            "          0/1 org desk'\n")
        f.close()
        self.p = Parser(self.nb_path)

    def test_get_nb_filename(self):
        self.assertEqual(
                self.p._get_nb_filename(datetime(2012, 10, 14)),
                os.path.join(self.nb_path,'2012-10.txt'))

    def test_parse_day_block(self):
        block = ['', '5', 'some stuff', '26', 'some other stuff']
        expected = {5: 'some stuff', 26: 'some other stuff'}
        self.assertEqual(self.p._parse_day_block(block), expected)

    def test_get_day_with_categories(self):
        """Get day 27."""
        expected = (
            "\n"
            "    Cat1: {Some shit: null}\n"
            "    text: '1/1 fix import sewan\n"
            "          2/2 check fidelidade, delete 0836\n"
            "          0/1 report incongruencias sewan pdf/cdr\n"
            "          1/1 fix b''illing db and run\n"
            "          0/2 guide entretien prestataire\n"
            "          0/1 org desk'\n")
        actual = self.p._get_day(datetime(2012, 10, 27))
        self.assertEqual(actual, expected)

    def test_get_day_without_categories(self):
        """Get day 21."""
        expected = (
            " {text: '1/1 fix import sewan\n"
            "    2/2 check fidelidade, delete 0836\n"
            "    0/1 org desk'}\n")
        actual = self.p._get_day(datetime(2012, 10, 21))
        self.assertEqual(actual, expected)

    def test_get_inexistant_day(self):
        """Get 14/10."""
        with self.assertRaises(EmptyDayException):
             self.p._get_day(datetime(2012, 10, 14))

    def test_get_inexistant_month(self):
        """Get 14/04."""
        with self.assertRaises(EmptyDayException):
             self.p._get_day(datetime(2012, 4, 14))

    def test_get_text_with_categories(self):
        block = (
            "\n"
            "    Cat1: {Some shit: null}\n"
            "    text: '1/1 fix import sewan\n"
            "          2/2 check fidelidade, delete 0836\n"
            "          0/1 report incongruencias sewan pdf/cdr\n"
            "          1/1 fix b''illing db and run\n"
            "          0/2 guide entretien prestataire\n"
            "          0/1 org desk'\n")
        expected = (
            "1/1 fix import sewan\n"
            "          2/2 check fidelidade, delete 0836\n"
            "          0/1 report incongruencias sewan pdf/cdr\n"
            "          1/1 fix b'illing db and run\n"
            "          0/2 guide entretien prestataire\n"
            "          0/1 org desk")
        self.assertEqual(self.p._get_text(block), expected)

    def test_get_text_without_categories(self):
        block = (
            " {text: '1/1 fix import sewan\n"
            "    2/2 check fidelidade, delete 0836\n"
            "    0/1 org desk'}\n")
        expected = (
            "1/1 fix import sewan\n"
            "    2/2 check fidelidade, delete 0836\n"
            "    0/1 org desk")
        self.assertEqual(self.p._get_text(block), expected)

    def test_get_pomodoros(self):
        # TODO
        pass

    def tearDown(self):
        os.remove(os.path.join(self.nb_path, '2012-10.txt'))



if __name__ == '__main__':
    unittest.main()
