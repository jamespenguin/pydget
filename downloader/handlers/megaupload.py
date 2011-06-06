#!/usr/bin/env python
#
# Pydget -
#  Megaupload Handler
#
import sys, time
import urllib, urllib2
import BeautifulSoup

def prepare_download(opener, page_url):
	# Get web page
	sys.stdout.write("[+] Grabbing web page, ")
	sys.stdout.flush()
	page = opener.open(page_url)
	print "Done"

	# Parse for CAPTCHA stuff, download links, etc
	sys.stdout.write("[+] Processing HTML, ")
	sys.stdout.flush()

	file_download_url = ""
	soup = BeautifulSoup.BeautifulSoup(page)

	for tag in soup.findAll("div"):
		if not tag.has_key("id"):
			continue
		if not tag["id"] == "downloadlink":
			continue
		link = tag.find("a")
		file_download_url = link["href"]

	print "Done"

	# Wait the requisite 45 seconds for free downloads
	print "[+] Waiting the required 45 seconds"

	last_line_length = 0
	for i in range(45, -1, -1):
		line = "[+] Time remaining: %d seconds" % i
		while len(line) < last_line_length:
			line += " "
		last_line_length = len(line)
		sys.stdout.write("\r%s" % line)
		sys.stdout.flush()
		time.sleep(1)
	print

	return file_download_url
