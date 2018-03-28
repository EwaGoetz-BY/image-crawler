#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import errno
import io
import os
import os.path
import sys
import unittest
import urllib.error
import urllib.parse

import imgcrawl


class TestDownloadImages(unittest.TestCase):
    def setUp(self):
        self.crawler = imgcrawl.ImgCrawler()
        self.download_dir = os.path.join(os.curdir, 'test_download_dir/')
        self.log_file = os.path.join(os.curdir, 'test_download.log')
        self.log_message = 'Hello World'
        self.url_file = 'test_urls.txt'
        self.urls = ['https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg',
                     'https://lh3.googleusercontent.com/u7kDXCIzqwieCqStzmg9CQgWsyltRCTf244HUFw_erDYamAhhSnd4P55szrR_vOLuM8gRkRn6rhHeq1rybiulqRcJcrIcBMAhqUBJ9MPHP2ezHJ6Ci9K4na0P6YAB0lgOy-YfpvWbjc',
                     'https://www.google.de/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',
                     'https://www.python.org/',
                     'http://foofoofoofoofoo.de/logo.svg',
                     'foo:upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg'
                    ]
        self.downloadable = 2

    def test_download_images_exception_handling(self):
        file_name = 'fake_name.txt'
        # suppress printing
        old_stderr, sys.stderr = sys.stderr, io.StringIO()

        # testing whether program gracefully exits and forwards error message on exception
        with self.assertRaises(SystemExit) as context:
            self.crawler.download_images(file_name, self.download_dir, self.log_file)
        self.assertEqual(context.exception.code, errno.ENOENT)

        # restore the old error output
        sys.stderr = old_stderr

    def test_robots_txt_permission_checking(self):
        # testing content download permission for page allowing robots
        url = 'https://upload.wikimedia.org/wikipedia/commons/6/66/Guido_van_Rossum_OSCON_2006.jpg'
        components = urllib.parse.urlparse(url)
        self.assertTrue(self.crawler.download_allowed(url, components.scheme, components.netloc))

        # testing content download permission for page without robots.txt
        url = 'http://www.miriamzilio.de/image/tigi/model_sfactor.jpg'
        components = urllib.parse.urlparse(url)
        self.assertTrue(self.crawler.download_allowed(url, components.scheme, components.netloc))

        # Google disallows crawling for their search page
        url = 'https://www.google.de/'
        components = urllib.parse.urlparse(url)
        self.assertFalse(self.crawler.download_allowed(url, components.scheme, components.netloc))

        # URL missing
        self.assertTrue(self.crawler.download_allowed('', 'https', 'upload.wikimedia.org'))

        # scheme missing
        url = 'https://upload.wikimedia.org/wikipedia/commons/6/66/Guido_van_Rossum_OSCON_2006.jpg'
        components = urllib.parse.urlparse(url)
        with self.assertRaises(urllib.error.URLError) as context:
            self.assertTrue(self.crawler.download_allowed(url, '', components.netloc))

        # netloc missing
        with self.assertRaises(urllib.error.URLError) as context:
            self.assertTrue(self.crawler.download_allowed(url, components.scheme, ''))

        # wrong type for crawler download
        with self.assertRaises(TypeError) as context:
            self.crawler.download_allowed(1, 'https', 'www.google.de')

        # URL does not exist
        url = 'http://foofoofoofoofoo.de/logo.svg'
        components = urllib.parse.urlparse(url)
        with self.assertRaises(urllib.error.URLError) as context:
            self.crawler.download_allowed(url, components.scheme, components.netloc)

    def test_logger_setup(self):
        # logger setup with default arguments
        self.assertFalse(os.path.exists(self.log_file))
        logger = self.crawler.setup_log(self.log_file)

        self.assertTrue(os.path.exists(self.log_file))
        self.assertTrue(os.path.isfile(self.log_file))

        logger.info(self.log_message)
        with open(self.log_file, 'r') as handle:
            self.assertTrue(handle.read().endswith(self.log_message + '\n'))
        os.remove(self.log_file)

        # trying to create a log file on a directory should cause the program to exit
        with self.assertRaises(IsADirectoryError) as context:
            self.crawler.setup_log(os.curdir)
        self.assertEqual(context.exception.errno, errno.EISDIR)

    def test_logger_shutdown(self):
        # logger setup with default arguments
        logger = self.crawler.setup_log(self.log_file)
        self.assertTrue(logger.handlers)
        self.crawler.shutdown_log(logger)
        self.assertFalse(logger.handlers)

    def test_image_download(self):
        # image download test with an example url file
        #     writing the URL file
        with open(self.url_file, 'w') as urls:
            urls.write('\n'.join(self.urls))

        #     crawling using the set up arguments
        self.crawler.download_images(self.url_file, self.download_dir, self.log_file)

        #     testing consistency between urls count and log file length
        with open(self.log_file) as log:
            for i, l in enumerate(log):
                pass
        self.assertEqual(i, len(self.urls))

        #     testing number of downloaded images versus expected outcome
        self.assertEqual(len(os.listdir(self.download_dir)), self.downloadable)

        #     removing files created while testing
        for image in os.listdir(self.download_dir):
            os.remove(os.path.join(self.download_dir, image)) 
        os.rmdir(self.download_dir)
        os.remove(self.log_file)
        os.remove(self.url_file)
        
    def tearDown(self):
        if os.path.exists(self.download_dir):
            for image in os.listdir(self.download_dir):
                os.remove(os.path.join(self.download_dir, image)) 
            os.rmdir(self.download_dir)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        if os.path.exists(self.url_file):
            os.remove(self.url_file)


if __name__ == '__main__':
    unittest.main()
