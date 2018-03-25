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

    def test_robots_txt_permission_checking(self):
        # testing content download permission for page allowing robots
        self.assertTrue(self.crawler.download_allowed('https://upload.wikimedia.org/wikipedia/commons/6/66/Guido_van_Rossum_OSCON_2006.jpg'))

        # testing content download permission for page without robots.txt
        self.assertTrue(self.crawler.download_allowed('http://www.miriamzilio.de/image/tigi/model_sfactor.jpg'))

        # Google disallows crawling for their search page
        self.assertFalse(self.crawler.download_allowed('https://www.google.de/'))

        # wrong type for crawler download
        self.assertFalse(self.crawler.download_allowed(1))

        # wrong type for crawler download
        self.assertFalse(self.crawler.download_allowed(''))

        # URL invalid
        self.assertFalse(self.crawler.download_allowed('http://foofoofoofoofoo.de'))


if __name__ == '__main__':
    unittest.main()
