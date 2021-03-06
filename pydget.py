#!/usr/bin/env python
#
# Pydget -
#  Main Interface Script
#
import os, sys
import argparse
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
#download_url = "http://www.megaupload.com/?d=Y9AQIX5V"
# mp4 video test
#download_url = "http://www.megaupload.com/?d=2A7OQPBC"

# DepositFiles
#download_url = "http://depositfiles.com/files/syljwwe1v"

# Hotfile
#download_url = "http://hotfile.com/dl/40926143/bfebc50/Linkin_Park_-_Meteora_-_01_-_Foreword.mp3.html"

# Oron
#download_url = "http://oron.com/whuctpz7kc1p/Linkin_Park_-_Waiting_For_The_End_%28DJ_Lynnwood_and_Dave_Dresden_Remix%29.mp3.html"

# Filesonic
download_url = "http://www.filesonic.com/file/1105360991/"

#!# End Config #!#

def process_arguments():
	global arguments
	parser = argparse.ArgumentParser(description="Pydget - Automate (for the most part) downloading files from file hosting websites!")
	parser.add_argument("download_urls", metavar="URL", type=str, nargs="+",
			    help="One or more URLs to download files from")
	parser.add_argument("--pause", action="store_true", default=False,
			    help="Wait for user input after a file finishes downloading, before beginning the next download.")
	parser.add_argument("--save-to", metavar="path", type=str, nargs=1, default=".",
			    help="Save downloaded files to a specific folder.")
	arguments = parser.parse_args()

if __name__ == "__main__":
	try:
		# process arguments
		process_arguments()

		# resolve output path
		if not os.path.exists(arguments.save_to[0]):
			print "[+] Output path does not exist, will try and make it!"
			try:
				os.mkdir(arguments.save_to[0])
			except:
				print "[!] Failed to create output directory provided, exiting..."
				sys.exit()

		# download files :)
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
			s = download_handler.session(url, arguments.save_to[0])
			s.download_file()

			if arguments.download_urls.index(url) != len(arguments.download_urls)-1:
				if arguments.pause:
					print "-" * 50
					raw_input("[+] Press enter to start downloading next file...")
	except KeyboardInterrupt:
		print
		sys.exit()
