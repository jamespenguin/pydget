Pydget
======

Pydget is a Python powered application for (mostly) automating the process of downloading files from various file hosting websites.

Also, Pydget was and still is developed primarily on an iPad using nano and a copy of Python compiled to run on iOS. 

Supported Websites
------------------

Pydget can be used to dwonload files from:

* [Depositfiles](http://depositfiles.com)
* [Megaupload](http://megaupload.com)
* [Hotfile](http://hotfile.com)

TODO
----

* Better command line and user interface stuff
* Fine tune downloading scripts
* Add support for more hosting websites
* Automate CAPTCHA input using Decaptcher.com

Usage
-----

    usage: pydget.py [-h] [--pause] [--save-to path] URL [URL ...]
    
    Pydget - Automate (for the most part) downloading files from file hosting websites!
    
    positional arguments:
      URL             One or more URLs to download files from
    
    optional arguments:
      -h, --help      show this help message and exit
      --pause         Wait for user input after a file finishes downloading,
                      before beginning the next download.
      --save-to path  Save downloaded files to a specific folder.