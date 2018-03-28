#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import errno
import unittest
import sys

import config
import imgcrawl


# small helper to suppress parser usage message
def exit_without_message(message=None):
    sys.exit(2)


# small helper to suppress parser help message
def print_no_help(file=None):
    pass


class TestParseArguments(unittest.TestCase):
    def setUp(self):
        self.parser = imgcrawl.make_parser()
        self.parser.error = exit_without_message
        self.parser.print_help = print_no_help

        self.ARGUMENT_COUNT = 3
        self.URL_FILE = 'links.txt'
        self.DOWNLOAD_DIR = 'download_dir/images/'
        self.LOG_FILE = 'download_dir/images.log'

    def test_parse_arguments_valid_input(self):
        # testing with only url file given, download directory and log file default
        arguments = imgcrawl.parse_arguments([self.URL_FILE])

        self.assertEqual(len(vars(arguments)), self.ARGUMENT_COUNT)
        self.assertEqual(arguments.url_file, self.URL_FILE)
        self.assertEqual(arguments.destination_dir, config.DEFAULT_DESTINATION_DIR)
        self.assertEqual(arguments.log_file, config.DEFAULT_LOG_FILE)

        # testing with url file and download directory given, log file default
        arguments = imgcrawl.parse_arguments([self.URL_FILE, '-d', self.DOWNLOAD_DIR])

        self.assertEqual(len(vars(arguments)), self.ARGUMENT_COUNT)
        self.assertEqual(arguments.url_file, self.URL_FILE)
        self.assertEqual(arguments.destination_dir, self.DOWNLOAD_DIR)
        self.assertEqual(arguments.log_file, config.DEFAULT_LOG_FILE)

        # testing all arguments given, different order
        arguments = imgcrawl.parse_arguments(['-d', self.DOWNLOAD_DIR, self.URL_FILE, '-l', self.LOG_FILE])

        self.assertEqual(len(vars(arguments)), self.ARGUMENT_COUNT)
        self.assertEqual(arguments.url_file, self.URL_FILE)
        self.assertEqual(arguments.destination_dir, self.DOWNLOAD_DIR)
        self.assertEqual(arguments.log_file, self.LOG_FILE)

    def test_parse_arguments_help(self):
        # testing help
        with self.assertRaises(SystemExit) as context:
            imgcrawl.parse_arguments(['-h'], self.parser)
        self.assertEqual(context.exception.code, 0)

    def test_parse_arguments_invalid_input(self):
        # testing with no arguments
        with self.assertRaises(SystemExit) as context:
            imgcrawl.parse_arguments([], self.parser)
        self.assertEqual(context.exception.code, errno.ENOENT)

        # testing with download directory and log file, but no url file given.
        with self.assertRaises(SystemExit) as context:
            imgcrawl.parse_arguments(['-d', self.DOWNLOAD_DIR, '-l', self.LOG_FILE], self.parser)
        self.assertEqual(context.exception.code, errno.ENOENT)

        # testing with wrong argument type
        with self.assertRaises(TypeError):
            imgcrawl.parse_arguments([self.URL_FILE, '-d', 404], self.parser)

        # testing faulty non-list argument
        with self.assertRaises(SystemExit) as context:
            imgcrawl.parse_arguments(self.URL_FILE, self.parser)
        self.assertEqual(context.exception.code, errno.ENOENT)


if __name__ == '__main__':
    unittest.main()
