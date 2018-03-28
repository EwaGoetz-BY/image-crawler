# -*- coding: utf-8 -*-

import os

# default paths
DEFAULT_DESTINATION_DIR = os.getcwd()
DEFAULT_LOG_FILE = 'crawling.log'

# command arguments help
DESCRIPTION = 'Download images from URL list in a file.'
HELP_URL_FILE = 'plaintext file containing URLs of images to download'
HELP_DESTINATION_DIR = 'specify alternative destination directory (default: current working directory)'
HELP_LOG_FILE = 'specify alternative log file (default: %s)'

# URL requests
IMAGE_MIMETYPE = 'image'

# robots.txt
ROBOTS = 'robots.txt'
USER_AGENT = '*'

# logging
LOG_FORMAT = '%(asctime)s %(message)s'
LOG_INITIAL_MESSAGE = 'downloading images from URLs listed in file "%s" into directory "%s".'
LOG_URL_INVALID = 'url string invalid'
LOG_ERROR_ROBOTS = 'unable to access URL'
LOG_DISALLOWED = 'download disallowed by robots.txt'
LOG_ERROR_OPENING = 'failed to open image URL'
LOG_NOT_AN_IMAGE = 'url content is not an image'
LOG_ERROR_DOWNLOADING = 'unable to download the image'
LOG_DOWNLOADED = 'downloaded'

# appearance
MAX_URL = 40
MAX_FILE_NAME = 15
PROGRESS_BAR_WIDTH = 30