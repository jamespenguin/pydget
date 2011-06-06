#!/usr/bin/env python
#
# Py-Downloader Testing Script
#
from downloader import download_handler
import sys

###
# Config
###
#download_url = "http://teh1337.nfshost.com/misc/Happy%20Hopper.MP3"
#download_url = "http://www.google.com/images/logos/ps_logo2.png"
download_url = "http://www.megaupload.com/?d=C5SOA1FD"

#!# End Config #!#

if __name__ == "__main__":
	try:
		s = download_handler.session(download_url)
	        s.download_file()
	except KeyboardInterrupt:
		print
		sys.exit()
