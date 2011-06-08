#!/usr/bin/env python
#
# Pydget -
#  Depositfiles Handler
#
import os, sys, time
import urllib, urllib2, urlparse
import BeautifulSoup
import form_grabber

def prepare_download(opener, page_url):
	# Get web page
	sys.stdout.write("[+] Grabbing web page, ")
	sys.stdout.flush()
	page = opener.open(page_url).read()
	print "Done"

	a = open("page.html", "w")
	a.write(page)
	a.close()

	# "click" the free download button
	sys.stdout.write("[+] Grabbbing download page, ")
	sys.stdout.flush()
	soup = BeautifulSoup.BeautifulSoup(page)
	form_action, data = form_grabber.process_form(soup, page_url, form_index=1, debug=True)
	data["submit"] = "FREE downloading"
	data = urllib.urlencode(data)
	request = urllib2.Request(form_action, data)
	response = opener.open(request).read()
	print "Done"

	# Parse for file download URL
	sys.stdout.write("[+] Parsing for file download URL, ")
	sys.stdout.flush()
	file_download_url = response.split("('#download_container').load('")[1]
	file_download_url = file_download_url.split("'")[0]
	file_download_url = urlparse.urljoin("http://depositfiles.com", file_download_url)
	print "Done"

	# Wait the requisite 60 seconds for free downloads
	print "[+] Waiting the required 60 seconds"
	last_line_length = 0
	for i in range(60, -1, -1):
		line = "[+] Time remaining: %d seconds" % i
		while len(line) < last_line_length:
			line += " "
		last_line_length = len(line)
		sys.stdout.write("\r%s" % line)
		sys.stdout.flush()
		time.sleep(1)
	print

	# get the ACTUAL file download link
	sys.stdout.write("[+] Retrieving final download link, ")
	sys.stdout.flush()
	page = opener.open(file_download_url).read()
	file_download_url = page.split("action")[1].split("=")[1]
	file_download_url = file_download_url.split("\"")[1].split("\"")[0]
	print "Done"

	return file_download_url
