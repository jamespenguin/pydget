#!/usr/bin/env python
#
# Pydget -
#  Main Interface Script
#
import sys, argparse
from downloader import download_handler

###
# Config
###
# Important variables, don't touch them!
arguments = None

# Testomg stuff
# Megaupload
# deb stuff
#download_url = "http://www.megaupload.com/?d=C5SOA1FD"
# mp3 test
download_url = "http://www.megaupload.com/?d=Y9AQIX5V"
# mp4 video test
download_url = "http://www.megaupload.com/?d=2A7OQPBC"

# DepositFiles
#download_url = "http://depositfiles.com/files/syljwwe1v"

# Hotfile
#download_url = "http://hotfile.com/dl/40926143/bfebc50/Linkin_Park_-_Meteora_-_01_-_Foreword.mp3.html"

#!# End Config #!#

def process_arguments():
	global arguments
	parser = argparse.ArgumentParser(description="Pydget - Automate (for the most part) downloading files from file hosting websites!")
	parser.add_argument("download_urls", metavar="URL", type=str, nargs="+",
			    help="One or more URLs to download files from")
	parser.add_argument("--pause", action="store_true", default=False,
		    help="Wait for user input after a file finishes downloading, before beginning the next download.")
	arguments = parser.parse_args()

if __name__ == "__main__":
	try:
		process_arguments()
		for url in arguments.download_urls:
			index = arguments.download_urls.index(url) + 1
			total = len(arguments.download_urls)
			print "=" * 70
			line = "| Starting download process for file %d of %d" % (index, total)
			while len(line) < 69:
				line += " "
			line += "|"
			print line
			print "=" * 70
			print "-" * 50
			s = download_handler.session(url)
			s.download_file()

			if arguments.download_urls.index(url) != len(arguments.download_urls)-1:
				if arguments.pause:
					print "-" * 50
					raw_input("[+] Press enter to start downloading next file...")
	except KeyboardInterrupt:
		print
		sys.exit()
