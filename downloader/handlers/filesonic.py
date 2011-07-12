#!/usr/bin/env python
#
# Pydget -
#  Filesonic Handler
#
import os, sys, time, md5
import urllib, urllib2, urlparse
import BeautifulSoup
import form_grabber

def prepare_download(opener, page_url):
	# Get web page
	sys.stdout.write("[+] Grabbing web page, ")
	sys.stdout.flush()
	page = opener.open(page_url).read()
	print "Done"

	# "click" the free download button
	sys.stdout.write("[+] Requesting free download, ")
	sys.stdout.flush()
	soup = BeautifulSoup.BeautifulSoup(page)
	link_tail = ""
	for tag in soup.findAll("a"):
		if not tag.has_key("id") or tag["id"] != "free_download":
			continue
		link_tail = tag["href"]
	download_request_link = urllib2.urlparse.urljoin(page_url, link_tail)
	now = int(time.time())
	data = {"tm":now,
		"tm_hash":md5.md5(str(now)).hexdigest()}
	request = urllib2.Request(download_request_link)
	request.add_header("Referer", page_url)
	response = opener.open(request).read()
	print "Done"

	# Get file name
	file_name = ""
	soup = BeautifulSoup.BeautifulSoup(response)
	for tag in soup.findAll("p"):
		if not tag.has_key("class") or tag["class"] != "fileInfo filename":
			continue
		file_name = tag.findAll("strong")[0].string
		file_name = file_name.replace("-", "_")
		break

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

	if "Start download now!" not in response:
		# Get CAPTCHA Image
		sys.stdout.write("[+] Grabbing CAPTCHA image, ")
		sys.stdout.flush()
		site_id = response.split("Recaptcha.create(\"")[1].split("\"")[0]
		captcha_request_url = "http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=0.21918660820070812" % site_id
		captcha_response_page = opener.open(captcha_request_url).read()
		captcha_challenge_field = captcha_response_page.split("challenge : ")[1].split(",")[0]
		captcha_challenge_field = captcha_challenge_field.replace("'", "")
		captcha_image_url = "http://www.google.com/recaptcha/api/image?c=%s" % captcha_challenge_field
		captcha_image_data = opener.open(captcha_image_url).read()
		captcha_image_file = open("image.jpg", "wb")
		captcha_image_file.write(captcha_image_data)
		captcha_image_file.close()
		print "Done"
	
		# get CAPTCHA answer
		print "[+] Open image.jpg, and type in the words below"
		captcha_answer = raw_input("[?] Answer: ")
		data = {}
		data["recaptcha_challenge_field"] = captcha_challenge_field
		data["recaptcha_response_field"] = captcha_answer
		data["submit"] = "submit"
	
		# POST response
		sys.stdout.write("[+] Sending CAPTCHA response to server, ")
		sys.stdout.flush()
		data = urllib.urlencode(data)
		action_url = urllib2.urlparse.urljoin(page_url, "?start=1")
		request = urllib2.Request(action_url, data)
		response = opener.open(request).read()
		print "Done"	

	# Get download URL
	sys.stdout.write("[+] Getting download URL, ")
	sys.stdout.flush()
	download_url = response.split("Start download now!")[0]
	download_url = download_url.split("href=")[-1]
	download_url = download_url.split("\"")[1]
	download_url = download_url.split("\"")[0]
	print "Done"

	return download_url, file_name