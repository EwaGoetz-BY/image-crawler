# -*- coding: utf-8 -*-

import errno
import io
import sys
import unittest

import imgcrawl


class TestDownloadImages(unittest.TestCase):
    def setUp(self):
        self.crawler = imgcrawl.ImgCrawler()

    def test_download_images_exception_handling(self):
        file_name = 'fake_name.txt'
        old_stderr, sys.stderr = sys.stderr, io.StringIO()

        # testing whether program gracefully exits and forwards error message on exception
        with self.assertRaises(SystemExit) as exit:
            self.crawler.download_images(file_name, None, None)
            self.assertEqual(exit.code, errno.ENOENT)
            self.assertEqual(sys.stderr.read(), "[Errno 2] No such file or directory: '%s'" % file_name)

        sys.stderr = old_stderr


if __name__ == '__main__':
    unittest.main()
