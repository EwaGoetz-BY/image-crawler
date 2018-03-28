#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import unittest

import progressbar


class TestProgressBar(unittest.TestCase):
    def setUp(self):
        # suppress printing bar
        self.output = io.StringIO()
        self.old_stdout, sys.stdout = sys.stdout, self.output
        
    def test_create_bar(self):
        # create bar with max 10 and bar width 20
        progressbar.ProgressBar(10, 20)
        self.assertTrue(self.output.getvalue().endswith('[00 / 10] |--------------------| 0.0%'))

        # wrong type used as max_malue raises a value error
        with self.assertRaises(ValueError):
            progressbar.ProgressBar('abc', 10)

        # wrong type used as max_malue raises a value error
        with self.assertRaises(TypeError):
            progressbar.ProgressBar(8, 'abc')

    def test_set_bar(self):
        # set bar to middle
        bar = progressbar.ProgressBar(8, 10)
        self.assertTrue(self.output.getvalue().endswith('[0 / 8] |----------| 0.0%'))
        bar.set(4)
        self.assertTrue(self.output.getvalue().endswith('[4 / 8] |=====-----| 50.0%'))
        
        # set bar to more than max
        bar.set(12)
        self.assertTrue(self.output.getvalue().endswith('[8 / 8] |==========| 100.0%'))

        # attemt to set bar with array instead of a numerical value
        with self.assertRaises(TypeError):
            bar.set([4])

    def test_bar_complete(self):
        # test completing the bar
        bar = progressbar.ProgressBar(5, 8)
        self.assertTrue(self.output.getvalue().endswith('[0 / 5] |--------| 0.0%'))
        bar.complete('done!')
        self.assertTrue(self.output.getvalue().endswith('[5 / 5] |========| 100.0% done!\n'))
        
    def tearDown(self):
        sys.stdout = self.old_stdout


if __name__ == '__main__':
    unittest.main()