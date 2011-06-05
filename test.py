#!/usr/bin/env python
#
# Py-Downloader Testing Script
#
from downloader import download_handler

###
# Config
###
download_url = "http://teh1337.nfshost.com/misc/Happy%20Hopper.MP3"
# "http://www.google.com/images/logos/ps_logo2.png"

#!# End Config #!#

if __name__ == "__main__":
	s = download_handler.session(download_url)
        s.download_file()
