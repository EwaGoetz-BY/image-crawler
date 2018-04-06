#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time

import config

class ProgressBar:
    """
    Displays progress bar, current value, and percentage (presuming count from 0 to max_value).
    """
    def __init__(self, max_value, width=30):
        """
        Progress bar constructor. Sets starting value for the progress bar and displays the initial empty bar.

        :param max_value: maximal (numerical) value at which the bar will reach 100 percent completion
        :type max_value: int, float
        :param width: optional width of the progress bar - a positive integer, defaults to 30
        :type width: int
        :return:
        """
        self.max_value = float(max_value)
        self.bar_width = width
        self.digits = math.ceil(math.log10(self.max_value + 1))
        self.text_format = '[%%0%dd / %d] |%%s%%s| %%.1f%%%%' % (self.digits, self.max_value)
        self.printed_characters = 0

        self.current_value = 0.0
        self.set(0.0)

    def set(self, value=1.0):
        """
        Updates the printed progress bar and counters by returning the carriage to the beginning of the line 
        and printing new progress value representation over it (in process again presuming counting from 0 to max)

        :param value: optional value by which to increase the current value, defaults to 1.0
        :type value: int, float
        :return:
        """
        self.current_value = float(value)
        self.current_value = max(min(self.current_value, self.max_value), 0.0)

        # clean the output
        print(self.printed_characters * '\r', end='', flush=True)

        # print the current status
        percentage = min(self.current_value / self.max_value * 100, 100.0)
        bars = int(math.floor(percentage * self.bar_width / 100.0))
        output = self.text_format % (self.current_value, bars * '=', (self.bar_width - bars) * '-', percentage)

        print(output, end='', flush=True)
        self.printed_characters = len(output)

    def complete(self, text=config.PROGRESS_COMPLETE):
        """
        Sets the progress to 100 percent and a comment upon completion

        :param text: optional comment or message to be printed, defaults to "completed"
        :type text: str, any printable
        :return:
        """
        self.set(self.max_value)
        print(' %s' % text)


if __name__ == '__main__':
    lines = 15
    bar = ProgressBar(lines)
    for i in range(lines):
        bar.set(i)
        time.sleep(0.2)
    bar.complete()
