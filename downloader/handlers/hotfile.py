#!/usr/bin/env python
#
# Pydget -
#  Hotfile Handler
#
import os, sys, time
import urllib, urllib2, urlparse
import BeautifulSoup
import form_grabber

def prepare_download(opener, page_url):
	# Get web page
	sys.stdout.write("[+] Grabbing web page, ")
	sys.stdout.flush()
	page = opener.open(page_url)
	print "Done"

	# Parse for download request form
	sys.stdout.write("[+] Parsing for download request form, ")
	sys.stdout.flush()
	soup = BeautifulSoup.BeautifulSoup(page)
	form_action, data = form_grabber.process_form(soup, page_url, form_index=1)
	wait_time = int(data["wait"])
	print "Done"

	# Wait the requisite nummber of seconds for free downloads
	print "[+] Waiting the required %d seconds" % wait_time
	last_line_length = 0
	for i in range(wait_time, -1, -1):
		line = "[+] Time remaining: %d seconds" % i
		while len(line) < last_line_length:
			line += " "
		last_line_length = len(line)
		sys.stdout.write("\r%s" % line)
		sys.stdout.flush()
		time.sleep(1)
	print

	# make a request to download the file
	sys.stdout.write("[+] Requesting to download file, ")
	sys.stdout.flush()
	data = urllib.urlencode(data)
	request = urllib2.Request(form_action, data)
	response = opener.open(request).read()
	soup = BeautifulSoup.BeautifulSoup(response)
	print "Done"

	if "You reached your hourly traffic limit." in response:
		print "[!] Hourly traffic limit reached!"
		return

	# check for CAPTCHA
	sys.stdout.write("[+] Processing CAPTCHA data, ")
	sys.stdout.flush()

	form_action, data = form_grabber.process_form(soup, page_url, form_index=1)

	captcha_iframe_url = soup.findAll("iframe")[0]["src"]
	captcha_iframe_page = opener.open(captcha_iframe_url)
	captcha_iframe_soup = BeautifulSoup.BeautifulSoup(captcha_iframe_page)
	form_action, data = form_grabber.process_form(captcha_iframe_soup, page_url)
	captcha_image_url = captcha_iframe_soup.findAll("img")[0]["src"]
	captcha_image_url = urlparse.urljoin(captcha_iframe_url, captcha_image_url)
	captcha_image_data = opener.open(captcha_image_url).read()

	a = open("image.jpg", "wb")
	a.write(captcha_image_data)
	a.close()

	print "Done"

	# get CAPTCHA answer
	print "[+] Open image.jpg, and type in the words below"
	captcha_answer = raw_input("[?] Answer: ")
	data["recaptcha_response_field"] = captcha_answer
	data["action"] = "checkcaptcha"

	# post response
	sys.stdout.write("[+] Sending CAPTCHA response to server, ")
	sys.stdout.flush()
	data = urllib.urlencode(data)
	request = urllib2.Request(form_action, data)
	response = opener.open(request).read()
	if "Wrong Code. Please try again." in response:
		print "Failed"
		return
	print "Done"	

	# parse out download URL
	file_download_url = ""
	soup = BeautifulSoup.BeautifulSoup(response)
	for tag in soup.findAll("a"):
		if not tag.has_key("class"):
			continue
		if tag["class"] == "click_download":
			file_download_url = tag["href"]

	return file_download_url
