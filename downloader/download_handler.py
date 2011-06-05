#!/usr/bin/env python
#
# Py-Downloader Main Downloading Class
#
import os, sys, time, math
import urllib, urllib2
import BeautifulSoup
import progressBar

class session:
	def __init__(self, download_url):
		self.__download_url = download_url
		self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#		self.__opener.addheaders = [("User-Agent", 
		self.__download_prepared = False

	def __get_easy_file_size(self, content_length):
		"""
		Turn a given file size in bytes, into a nice human readable number.
		1024 bytes => 1Kb
		"""

		units = ["Kb", "Mb", "Gb", "Tb", "Pb", "Yb"]
		unit = "Bytes"
		count = 0
		while len(str(int(content_length))) > 3:
			content_length /= 1024.0
			try:
				unit = units[count]
			except:
				unit = "Unknown"
			count += 1
		return "%.2f %s" % (content_length, unit)

	def __prepare_download(self):
		"""
		Prepare the file to be downloaded, by selecting things like 
		"free" download mode, and waiting through any download timers.
		"""
		# Do some stuff
		self.__download_prepared = True

	def download_file(self):
		"""
		Once the download has been prepared, actually download it.
		"""
		if not self.__download_prepared:
			self.__prepare_download()
		print "[+] Starting download for: %s" % self.__download_url

		# Request the file, and process its meta data
		response = self.__opener.open(self.__download_url)
		meta_info = response.info()
                content_length = int(response.headers["Content-Length"])
		file_name = os.path.split(self.__download_url)[1]
		file_name = urllib.unquote_plus(file_name)
		file_size = self.__get_easy_file_size(content_length)

		# Download the file, and save it to disc
                print "[+] Downloading file: %s (%s)" % (file_name, file_size)
		file_path = file_name # eventually make this changeable
		file_out = open(file_path, "wb")
		received_data_size = 0
		bar = progressBar.progressBar(content_length)
		last_size_check = 0
		last_chunk_time = time.time()
		last_line_len = 0

		while received_data_size != content_length:
			# Update status
			if time.time() - last_chunk_time >= 0.35:
				last_chunk_time = time.time()
				download_speed = received_data_size - last_size_check
				speed_string = "%s/s" % self.__get_easy_file_size(download_speed)
				last_size_check = received_data_size
				line = "\r[+] %s %s" % (bar.get_bar(received_data_size), speed_string)
				while len(line) < last_line_len:
					line += " "
				last_line_len = len(line)
				sys.stdout.write(line)
				sys.stdout.flush()

			# Get a chunk
			received_chunk = response.read(1024)
			received_data_size += len(received_chunk)
			file_out.write(received_chunk)

		file_out.close()
		sys.stdout.write("\r[+] %s              " % bar.get_bar(content_length))
		sys.stdout.flush()
		print "\n[+] Download Complete!"
