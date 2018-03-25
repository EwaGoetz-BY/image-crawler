#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import urllib.robotparser
from urllib.parse import urlparse

import constants


class ImgCrawler:
    """
    Image crawler for batch downloading images given by a list of URLs read from a plaintext file.
    """
    def __init__(self):
        self.robot = urllib.robotparser.RobotFileParser()

    def _download_images(self, url_file, destination_dir, log_file):
        """
        Internal implementation of the image downloading. Opens the URLs file and iterates over each URL.

        :param url_file: file name or path to the file with URLs
        :type url_file: str
        :param destination_dir: path to directory in which to store the images
        :type destination_dir: str
        :param log_file: file name or path to the log file
        :type log_file: str
        :return:
        """
        # opening the url file and reading the urls
        with open(url_file, 'r') as urls:
            for line in urls:
                if not self.download_allowed(url):
                    continue
                pass

    def download_images(self, url_file, destination_dir, log_file):
        """
        Downloads images from URLs given by the url_file, stores them into the directory destination_dir,
        and logs the progress in the log_file.

        :param url_file: file name or path to the file with URLs
        :type url_file: str
        :param destination_dir: path to directory in which to store the images
        :type destination_dir: str
        :param log_file: file name or path to the log file
        :type log_file: str
        :return:
        """
        try:
            self._download_images(url_file, destination_dir, log_file)
        except IOError as error:
            sys.stderr.write(str(error))
            sys.exit(error.errno)
        except Exception as error:
            sys.stderr.write('[Unknown error] %s' % str(error))
            sys.exit(1)

    def download_allowed(self, url):
        components = urlparse(url)
        self.robot.set_url('%s://%s/%s' % (components.scheme, components.netloc, constants.ROBOTS))
        self.robot.read()
        return self.robot.can_fetch(constants.USER_AGENT, url)

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
    pass
    # arguments = parse_arguments()
    # ImgCrawler().download_images(arguments.url_file, arguments.destination_dir, arguments.log_file)
