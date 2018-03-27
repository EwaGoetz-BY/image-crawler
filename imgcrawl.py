#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os.path
import sys
import urllib.error
import urllib.parse
import urllib.robotparser

import constants


class ImgCrawler:
    """
    Image crawler for batch downloading images given by a list of URLs read from a plaintext file.
    """

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
        logger = self.setup_log(log_file)
        logger.info(constants.LOG_INITIAL_MESSAGE % (url_file, destination_dir))

        download_count = 1

        # opening the url file and reading the urls
        with open(url_file, 'r') as urls:
            for url in urls:

                url = url.strip()
                components = urllib.parse.urlparse(url)
                if not (components.scheme and components.netloc and components.path):
                    logger.error('url string invalid: "%s"' % url)
                    continue
            
                # check whether the robots.txt allows us to crawl this URL
                try:
                    can_fetch = self.download_allowed(url, components.scheme, components.netloc, logger)
                except (AttributeError, urllib.error.URLError, ValueError):
                    logger.error('unable to access URL: %s' % url)
                    continue

                # log that image download is disallowed
                if not can_fetch:
                    logger.error('download disallowed by robots.txt: %s' % url)
                    continue

        # release the logger handles
        self.shutdown_log(logger)

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

    def download_allowed(self, url, scheme, netloc):
        """
        Checks the passed URL for crawling compliance with the robots.txt of the host

        :param url: the URL to be checked for robots.txt crawling compliance
        :type url: str
        :param scheme: the URL scheme
        :type scheme: str
        :param netloc: the URL netloc
        :type netloc: str
        :return: a flag indicating whether the download is allowed
        :rtype: bool
        """
        robot = urllib.robotparser.RobotFileParser('%s://%s/%s' % (scheme, netloc, constants.ROBOTS))
        try:
            robot.read()
        except ValueError:
            raise urllib.error.URLError('<urlopen error no protocol given>')

        return robot.can_fetch(constants.USER_AGENT, url)

        
    def setup_log(self, log_file):
        """
        Creates a log object for protocolizing the image downloads.
        The log file will be created unter the name and path given by the log_file argument.

        :param log_file: file name or path to the log file
        :type log_file: str
        :return: logger object enabling writing log entries
        :rtype: logging.Logger
        """
        directory = os.path.dirname(log_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        logger = logging.getLogger(log_file)
        formatter = logging.Formatter(constants.LOG_FORMAT)

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        return logger

    def shutdown_log(self, logger):
        """
        Releases the log file handle(s) for a given logger
        
        :param logger: logger object with resource handles
        :type logger: logging.Logger
        :return:
        """
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()


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
    arguments = parse_arguments()
    ImgCrawler().download_images(arguments.url_file, arguments.destination_dir, arguments.log_file)
