#! /usr/bin/env python2.7 
<<<<<<< HEAD
#
# FtpH : A Command Line Interface handler for your FTPs
# 
# Git Repository: github.com/StefanoBelli/ftp-handler
# 
# To get latest releases:
# execute - git pull in ftp-handler/ local repository
#
# { Version: devel }
# { Update Date: DD/MM/YYYY - 15/06/2015 } 
# { Status: DEVELOPMENT }
#
# Developer(s):
#  ---> StefanoBelli
#  \____mailto: <stefano9913@gmail.com>
#   \___GooglePlus: <plus.google.com/+StefanoBelli>
#    \__Website : <http://inthebit.it>
#
# to get latest update, go to ftp-handler/ local directory and execute 'git pull' inside this directory :)
#
=======
#ciao
>>>>>>> 92f60a45d4e2bcb7df2971777bad09853af4893a

#Needed modules
from ftplib import FTP
from ftplib import error_perm
import os
import sys
import re
import time
from socket import gaierror
import getpass

##Arguments by command line prompt##
arg_counter = int(len(sys.argv))

#Init ftpsrv var
global ftpsrv
debuglevel = 0

#Version info
version = "devel" 
udate = "15/06/2015"

#Banner
banner = '''
  _____ _____ ____  _   _ 
 |  ___|_   _|  _ \| | | |
 | |_    | | | |_) | |_| |
 |  _|   | | |  __/|  _  |
 |_|     |_| |_|   |_| |_|
                          
A simple FTP Manager for your FTPs, from Command Line! :) 
	
	Version: %s
	Update date: %s
'''%(str(version), udate)

#Help page
helppage = '''
FTPH: FTP Manager
++++++++++++++++++
Usage: [./ftph.py] <url/help> (debug level)
++++++++++++++++++
url/help: Type ftp server URL (like this: ftp.site.com) / --help, to type this help page.
debug level: Defines how many debug messages the FTP server should show. It is not compulsory, see below.
++++++++++++++++++
Debug Values: integer
|___________1 : minimum debug level
|___________>= 2 : higher debug level
If you don't declare any debug level, the value is 0
'''

os.system("clear")
#Anyway print banner
print banner

#############################ARGUMENT CHECK#######################################################
#KeyboardInterrupt
try:
	#Checks URL argument
	try:
		arg_url_ftp = str(sys.argv[1])
		if arg_url_ftp == "--help":
			print helppage
			sys.exit(0)
		else:
			pass
	except IndexError:
		print "\033[31m * \033[0m You need to type ftp url at least. Try '--help'\n"
		sys.exit(1)
	except ValueError:
		print "\033[31m * \033[0m This wasn't expected.\n [verr_arg_url_ftp]"
		sys.exit(1)

	#Checks debugging argument
	try:
		arg_debug = int(sys.argv[2])
		debuglevel = arg_debug
		if debuglevel == 1: 
			print "\033[32m * \033[0m Arguments: "+str(arg_counter)+"\n"
			print "\033[34m * \033[0m Debug level: "+str(debuglevel)+", minimum"
			pass
		elif debuglevel >= 2:
			print "\033[32m * \033[0m Arguments: "+str(arg_counter)+"\n"
			print "\033[34m * \033[0m Debug level: "+str(debuglevel)+", high" 
			pass
		elif debuglevel == 0:
			pass
		else:
			pass
	except IndexError:
		pass

	except ValueError:
		print "\n\033[31m * \033[0m Debug level needs to be integer.\n" 
		sys.exit(1)
#...
except KeyboardInterrupt:
	print "\n\033[33m * \033[0m Force closed by user [KeyboardInterrput]"
	sys.exit(2)
except SyntaxError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Syntax] mistake, not yours! :) \n"
	sys.exit(1)
except TypeError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Type, var] mistake, not yours! :) \n"
	sys.exit(1)
except IOError:
	print "\n\033[31m * \033[0mInput/Output error!\n"
	sys.exit(1)
except AttributeError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Attribute] mistake, not yours! :) \n"
	sys.exit(1)


####################################################################################################

#Connect()
def connect(url, dbl):
	print "\033[33m * \033[0m Trying to connect to: "+str(arg_url_ftp)+", wait..."
	try:
		global ftpsrv
		ftpsrv = FTP(str(url))	
		ftpsrv.set_debuglevel(dbl)
		ftpsrv.connect()
	except gaierror:
		print "\n\033[31m * \033[0m Error! Server wasn't reachable!\n\033[33m * \033[0m Try --help to get more infos\n"
		sys.exit(3)
	print "\033[32m * \033[0m Succesfully connected to %s! \n"%url
	time.sleep(1)

#Login 
def login(strurl):
	try:
		print "************LOGIN @ %s**********************************************************" %strurl
		print "=To connect anonymously, leave empty username and password"
		print "=But remember that if you login as anonymous you can't do something"
		print "=Such as copy, delete, rename files/directory, upload files."
		print "=And some servers don't accept Anonymous users."
		print "==Password is NOT shown=="
		username = str(raw_input("* Username: "))
		password = str(getpass.getpass("* Password: "))
		print "********************%s**********************************************************" %strurl
		time.sleep(1)
		os.system("clear")
		ftpsrv.login(username, password)
	except error_perm:
		print "\n\033[31m *\033[0m Username and password are wrong! Or in some cases only anonymous login is allowed.\n"
		sys.exit(3)
	if username == "" and password == "":
		print "\033[32m *\033[0m You logged in as Anonymous... remember that you can't do many things :) Enjoy\n"
		time.sleep(1)
	elif username == "root":
		print "\033[33m *\033[0m You are now 'ROOT', be responsible!\n"
		time.sleep(1)
	else:
		print "\033[32m *\033[0m Hello, %s, you logged in @ %s ;)\n" %(username, strurl)
		time.sleep(1)

#Mainf, all start here
def mainf():
	connect(arg_url_ftp, debuglevel)
	login(arg_url_ftp)

##Hello! :D##
try:
	mainf()
except KeyboardInterrupt:
	print "\n\033[34m * \033[0mUser exited.\n"
	sys.exit(2)
except SyntaxError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Syntax] mistake, not yours! :) \n"
	sys.exit(1)
except TypeError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Type, var] mistake, not yours! :) \n"
	sys.exit(1)
except IOError:
	print "\n\033[31m * \033[0mInput/Output error!\n"
	sys.exit(1)
except AttributeError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Attribute] mistake, not yours! :) \n"
	sys.exit(1)

