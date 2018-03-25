#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import constants


def make_parser():
    """
    Create an argument parser.
    The positional argument is the URLs text file.
    The optional arguments are the destination directory and the log file, defaulting to current working directory and 'download.log' respectively.

    :return: a parser object
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Download images from URL list in a file.')
    parser.add_argument('url_file', metavar='URL_FILE', type=str,
                        help='plaintext file containing URLs of images to download')
    parser.add_argument('-d', metavar='DEST_DIR', dest='destination_dir', default=constants.DEFAULT_DESTINATION_DIR, type=str,
                        help='specify alternative destination directory (default: current working directory)')
    parser.add_argument('-l', metavar='LOG_FILE', dest='log_file', default=constants.DEFAULT_LOG_FILE, type=str,
                        help='specify alternative log file (default: %s)' % constants.DEFAULT_LOG_FILE)

    return parser


def parse_arguments(argv=None, parser=None):
    """
    Parse the command line arguments or custom arguments.
    Optionally specify a custom parser. (Here used to suppress the verbose usage output while testing failing cases.)

    :param argv: arguments to be parsed, example: ['urls.txt', '-d', 'download_dir', '-l', 'img_download.log'], defaults to sys.argv[1:].
    :type argv: list of str
    :param parser: optional argument parser, if none is passed a new one is created using make_parser()
    :type parser: argparse.ArgumentParser
    :return: a key-value object populated with the given arguments and/or default values
    :rtype: argparse.Namespace
    """

    if parser is None:
        parser = make_parser()

    return parser.parse_args(argv)


if __name__ == '__main__':
    parse_arguments()
