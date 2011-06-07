#!/usr/bin/env python
#
# Pydget -
#   Global Downloading Handler Class
#
import os, sys, time, math
import threading
import urllib, urllib2, urlparse
import progressBar
import handlers.megaupload
import handlers.depositfiles

class session:
	def __init__(self, download_url):
		self.__download_url = download_url
		self.__file_download_url = "" # The URL of the actual FILE to download
		self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		self.__opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008092215 Firefox/3.0.1")]
		self.__download_prepared = False
		self.__status_line = ""
		self.__show_status = False
		self.__hosts = ["megaupload", "depositfiles"]

	def __display_status_bar(self):
		while self.__show_status:
			sys.stdout.write("\r%s" % self.__status_line)
			sys.stdout.flush()
			time.sleep(0.2)
		sys.stdout.write("\r%s" % self.__status_line)
		sys.stdout.flush()

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

	def __seconds_to_HMS(self, seconds):
		"""
		Turn a given number of seconds into a nice human readable
		HH:MM:SS format.
		"""

		minutes = seconds / 60
		remaining_seconds = seconds % 60
		hours = minutes / 60
		remaining_minutes = minutes % 60
		if hours:
        	        return "%02d:%02d:%02d" % (hours, remaining_minutes, remaining_seconds)
		return "%02d:%02d" % (minutes, remaining_seconds)

	def __prepare_download(self):
		"""
		Prepare the file to be downloaded, by selecting things like 
		"free" download mode, and waiting through any download timers.
		"""

		# determine what (if any) file hosting site the file is on
		sys.stdout.write("[+] Determining file hosting site, ")
		sys.stdout.flush()

		url_host = urlparse.urlparse(self.__download_url)[1]
		if url_host.startswith("www"):
			url_host = url_host[4:]
		url_host = url_host.split(".")[0]

		if url_host not in self.__hosts:
			print "Failed"
			print "[!] File host not found in list of supported hosts."
			return
		print "Done"
		print "[+] Host is: %s" % url_host.title()

		# Prepare the file download
		print "[+] Preparing file download"

		if url_host == "megaupload":
			file_download_url = handlers.megaupload.prepare_download(self.__opener, self.__download_url)
		elif url_host == "depositfiles":
			file_download_url = handlers.depositfiles.prepare_download(self.__opener, self.__download_url)

		self.__file_download_url = file_download_url

		self.__download_prepared = True

#		self.__file_download_url = self.__download_url

	def download_file(self):
		"""
		Once the download has been prepared, actually download it.
		"""
		if not self.__download_prepared:
			self.__prepare_download()

#		return

		# Request the file, and process its meta data
		file_name = os.path.split(self.__file_download_url)[1]
		file_name = urllib.unquote_plus(file_name)
		print "[+] Starting download for: %s" % file_name
		# print self.__file_download_url

		sys.stdout.write("[+] Gathering meta data, ")
		sys.stdout.flush()
		response = self.__opener.open(self.__file_download_url)
		meta_info = response.info()
		print "Done"
                content_length = int(response.headers["Content-Length"])
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
		self.__show_status = True
		self.__status_line = bar.get_bar(0)
		threading.Thread(target=self.__display_status_bar, args=()).start()

		while received_data_size != content_length:
			# Update status
			if time.time() - last_chunk_time >= 0.25:
				# calculate download speed
				last_chunk_time = time.time()
				download_speed = received_data_size - last_size_check
				download_speed *= 4

				# calculate remaining time
				remaining_bytes = content_length - received_data_size
				remaining_seconds = remaining_bytes / download_speed
				remaining_string = self.__seconds_to_HMS(remaining_seconds)

				# build status line
				speed_string = "%s/s" % self.__get_easy_file_size(download_speed)
				last_size_check = received_data_size
				line = "\r%s %s ETA: %s" % (bar.get_bar(received_data_size), speed_string, remaining_string)
				while len(line) < last_line_len:
					line += " "
				last_line_len = len(line)
				self.__status_line = line

			# Get a chunk
			received_chunk = response.read(1024)
			received_data_size += len(received_chunk)
			file_out.write(received_chunk)

		file_out.close()

		line = "\r%s" % bar.get_bar(content_length)
		while len(line) < last_line_len:
			line += " "
		self.__status_line = line
		self.__show_status = False
		while threading.activeCount() > 1:
			time.sleep(0.1)
		print "\n[+] Download Complete!"
