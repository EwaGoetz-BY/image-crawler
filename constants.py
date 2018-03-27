# -*- coding: utf-8 -*-

import os

# default paths
DEFAULT_DESTINATION_DIR = os.getcwd()
DEFAULT_LOG_FILE = 'imgcrawl.log'

# robots.txt
ROBOTS = 'robots.txt'
USER_AGENT = '*'

# logging
LOG_FORMAT = '%(asctime)s %(message)s'
LOG_INITIAL_MESSAGE = 'downloading images from URLs listed in file "%s" into directory "%s".'
