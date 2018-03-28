Image Crawler
=============

This small Python application downloads images from a set of URLs listed in a text file.

Usage
-----

``./imgcrawl.py [-h] URL_FILE [-d DESTINATION_PATH] [-l LOG_FILE_PATH]``

The `URL_FILE` parameter specifies the plaintext file containing URLs of images to download, written one per line, e.g.:

::

    http://mywebserver.com/images/271947.jpg
    http://mywebserver.com/images/24174.jpg
    http://somewebsrv.com/img/992147.jpg
    

The `-d` option allows specification of an alternative destination directory for storing the downloaded images. (Default: current working directory) 

The `-l` option allows specification of an alternative download log file. (Default: download.log)

Requirements
------------

Python 3
