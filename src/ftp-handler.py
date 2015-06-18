#! /usr/bin/env python2.7 
#
# FtpH : A Command Line Interface handler for your FTPs
# 
# Git Repository: github.com/StefanoBelli/ftp-handler
# 
# To get latest releases:
# execute - git pull in ftp-handler/ local repository
#
# { Version: 0.5 }
# { Update Date: DD/MM/YYYY - 19/06/2015 } 
# { Status: [FINAL DEVELOPMENT STAGE] }
#
# Developer(s):
#  ---> StefanoBelli
#  \____mailto: <stefano9913@gmail.com>
#   \___GooglePlus: <plus.google.com/+StefanoBelli>
#    \__Website : <http://inthebit.it>
#
# to get latest update, go to ftp-handler/ local directory and execute 'git pull' inside this directory :)
#

#
## TO-DO
#\__Write the help page ('h')
# \__Check for errors
#  \__Error Handling
#   \__Get a better output format (colors, syntax...)
#    \__Code syntax (spaces, useless lines...)
#    ~~Then~~
#     \==>Get a 1.0 version ;) 
# 

#Needed modules
import os
import sys
from ftplib import FTP
from ftplib import error_perm
from ftplib import error_temp
from re import split
from time import sleep
from time import localtime
from socket import gaierror
from socket import gethostbyname
from getpass import getuser
from getpass import getpass 

##Arguments by command line prompt##
arg_counter = int(len(sys.argv))
############

#Get local user
getluser = str(getuser())

#Get ip address
global getsrvip

#Init ftpsrv var
global ftpsrv
debuglevel = 0

#Used for naming users right
global srvuser
srvuser = ""

#Localtime
global lgtime
lgtime = localtime()

#Version info
version = float(0.5) 
udate = "19/06/2015"

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
=====================================HELP PAGE===============================================================
FTPH: FTP Manager
++++++++++++++++++
Usage: [./ftph.py] <url/help> (debug level)
++++++++++++++++++
url/help: Type ftp server URL (like this: ftp.site.com) / --help, to type this help page.
debug level: Defines how many debug messages the FTP server should show. It is not compulsory, see below.
***WARNING: TO SEE HOW TO USE FTPH BROWSER, TYPE COMMAND 'h' (to see how to use other commands) WHEN YOU GET INTO THE FTP***
++++++++++++++++++
Debug Values: integer
|___________1 : minimum debug level
|___________>= 2 : higher debug level
If you don't declare any debug level, the value is 0
++++++++++++++++++
Example: 
ftph ftp.debian.org   (Debug level will be null)
ftph ftp.debian.org 1 (Debug level will be min)
ftph ftp.debian.org 2 (Debug level will be max)
++++++++++++++++++
Developer: 
Stefano Belli
\_-> GitHub: <https://github.com/StefanoBelli>
 \_-> Google+: <https://plus.google.com/+StefanoBelli>
  \_-> mailto: <stefano9913@gmail.com>
   \_-> Website: <http://www.inthebit.it>
+++++++++++++++++++
FTPH Repository: <https://github.com/StefanoBelli/ftp-handler
'''

os.system("clear")
#Anyway print banner
print banner

#############################ARGUMENT CHECK#######################################################
try:
	#Checks URL argument
	try:
		arg_url_ftp = str(sys.argv[1])
		if arg_url_ftp == "--help":
			print helppage
			sys.exit(0)
		else:
			getsrvip = gethostbyname(arg_url_ftp)
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
	pass
except AttributeError:
	print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Attribute] mistake, not yours! :) \n"
	sys.exit(1)

####################################################################################################

#Connect and check...
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
	print "\033[32m * \033[0m Succesfully connected to %s - [IP: %s] \n"%(url, getsrvip)
	sleep(1)

#Login to the connected server
def login(strurl):
	try:
		global username
		print "************LOGIN @ %s**********************************************************" %strurl
		print "=To connect anonymously, leave empty username and password"
		print "=But remember that if you login as anonymous you can't do something"
		print "=Such as copy, delete, rename files/directory, upload files."
		print "=And some servers don't accept Anonymous users."
		print "==Password is NOT shown=="
		username = str(raw_input("* Username: "))
		password = str(getpass("* Password: "))
		print "********************%s**********************************************************" %strurl
		sleep(1)
		ftpsrv.login(username, password)
	except error_perm:
		os.system("clear")
		print "\n\033[31m *\033[0m Username and password are wrong! Or in some cases only anonymous login is allowed.\n"
                sleep(1)
		sys.exit(3)
	if username == "" and password == "":
		os.system("clear")
		print "\033[31m******\033[0mUse 'h' command to get help\033[31m******\033[0m"
		print "\033[32m *\033[0m You logged in as Anonymous... remember that you can't do many things :) Enjoy\n"
	elif username == "root":
		os.system("clear")
		print "\033[31m******\033[0mUse 'h' command to get help\033[31m******\033[0m"
		print "\033[33m *\033[0m Hello, %s you are now \033[31mroot\033[0m@%s, be responsible!\n" %(getluser, strurl)
	else:
		os.system("clear")
		print "\033[31m******\033[0mUse 'h' command to get help\033[31m******\033[0m"
		print "\033[32m *\033[0m Hello, %s, you logged in @ %s ;)\n" %(username, strurl)	

#FTP Browser (CLI)
def ftpWelcome(strurl, username):
	if username != "":
		srvuser = username
	elif username == "root":
		srvuser = "root"
	else:
		srvuser = "anonymous user"
	#Logged-In from
	print "\033[32m*\033[0m"
	print "\033[32m*\033[0m \O.O/<_______________"
	print "\033[32m*\033[0m  | | <Logged in from|"
	print "\033[32m*\033[0m  / \ <---------------"
	print "\033[32m*\033[0m %s:%s:%s on %s/%s/%s" %(lgtime.tm_hour, lgtime.tm_min, lgtime.tm_sec, lgtime.tm_year, lgtime.tm_mon, lgtime.tm_mday)
	print "\033[32m*\033[0m"
	print "\033[32m+-----~Welcome to~[\033[0m\033[34m%s\033[0m\033[32m]~that says-----------+\033[0m" %strurl 
	print ftpsrv.getwelcome()
	print "\033[32m+---------~~~[\033[0mIP:\033[34m%s\033[0m\033[32m]~~~--------------------+\033[0m" %getsrvip
	prompt(srvuser)
	return srvuser

#Prompt (FTP Browser prompt)
def prompt(suser):
	dirr = ftpsrv.nlst()
	print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip)
	print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
	for i in range(len(dirr)):
		print ">>> "+str(dirr[i])
	print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
	print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip) 
	prompt = raw_input(">>> ")
	checkPrompt(prompt)
	while (prompt != "ex"):
		os.system("clear")
		dirr = ftpsrv.nlst()
		print ""
		print "\033[32m*\033[0m Logged in from: %s:%s:%s on %s/%s/%s" %(lgtime.tm_hour, lgtime.tm_min, lgtime.tm_sec, lgtime.tm_year, lgtime.tm_mon, lgtime.tm_mday)
		print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip)
		print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
		for i in range(len(dirr)):
			print ">>> "+str(dirr[i])
		print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
		print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip) 
		prompt = raw_input(">>> ")
		checkPrompt(prompt)

#If statement for prompt
def checkPrompt(prompt):
        #For each statement error_perm, error_perm, IndexError
	#Add h command to get help

	###Check the prompt input###
	rechk = split('\s|(?<!\d)[,](?!\d)',prompt)

	#Exit command
	if prompt == "ex":
		print "\033[33m*\033[0m Closing connection..."
		ftpsrv.quit()
		print "\033[32m*\033[0m Bye bye! "
		sys.exit(0)

	#OS Shell
	elif prompt == "osh":
		print "\033[32m*\033[0m Switching to sh... Type exit to get back here :) "
		os.system("sh")

	#Change Directory command
	elif rechk[0] == "cd":
		ftpsrv.cwd(str(rechk[1]))

	#Remove Direcotory command
	elif rechk[0] == "rd":
		ftpsrv.rmd(str(rechk[1]))

	#RemoveFile command
	elif rechk[0] == "rf":
		ftpsrv.delete(str(rechk[1]))

	#Size of file command
	elif rechk[0] == "sz":
		fsize = ftpsrv.size(str(rechk[1]))
		print "File %s is big: %s Byte(s)" %(str(rechk[1]), str(fsize))
		raw_input("Press any key to get back...")

	#Make Directory command
	elif rechk[0] == "md":
		ftpsrv.mkd(str(rechk[1]))
	
	#Rename File & Directories 
	elif rechk[0] == "rn":
		ftpsrv.rename(str(rechk[1]), str(rechk[2]))
	
	#List directories
	elif rechk[0] == "als":
		dirname = str(rechk[1])
		print "*-*-*-*-*\033[34mListing directory: %s\033[0m*-*-*-*-*" %dirname
		ftpsrv.dir(dirname)
		raw_input("Press any key to continue... ")
	
	#FTP Command Execution
	elif rechk[0] == "fcmd":
		ftpsrv.sendcmd(str(rechk[1]))
		raw_input("===END OF OUTPUT===\nPress any key to get back....")
	
	#Get Binary file (non ASCII) from FTP
	elif rechk[0] == "dlb":
		dlfile = open(str(rechk[2]), "wb").write
		print "\033[32m*\033[0m Downloading: "+str(rechk[1])+"..."
		print "\033[33m*\033[0m Requested file "+"'"+str(rechk[1])+"'"+" size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
		ftpsrv.retrbinary("RETR "+str(rechk[1]), dlfile)
		print "\033[32m*\033[0m Downloaded file: "+os.getcwd()+"/"+rechk[2]
		raw_input("Press any key to continue...")

	#Upload Binary file (non ASCII) to FTP
	elif rechk[0] == "ulb":
		if os.access(str(rechk[1]), os.F_OK):
			print "\033[32m*\033[0m File exists"
			ulfile = open(str(rechk[1]), "rb")
		        print "\033[32m*\033[0m Uploading: "+str(rechk[1])+"..."
			ftpsrv.storbinary('STOR '+str(rechk[1]), ulfile)
			print "\033[32m*\033[0m Uploaded file "+"'"+str(rechk[1])+"'"+" which size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
			raw_input("Press any key to get back")
		else:
			print "\033[31m*\033[0m Your file doesn't exists"
			raw_input("Press any key to get back")

	#Get ASCII Lines from FTP
	elif rechk[0] == "dla":
		dlfile = open(str(rechk[2]), "wb").write
		print "\033[32m*\033[0m [ASCII Mode]Downloading: "+str(rechk[1])+"..."
		print "\033[33m*\033[0m Requested file "+"'"+str(rechk[1])+"'"+" size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
		ftpsrv.retrlines("RETR "+str(rechk[1]), dlfile)
		print "\033[32m*\033[0m Downloaded file: "+os.getcwd()+"/"+rechk[2]
		raw_input("Press any key to continue...")

	#Upload ASCII Lines to FTP
	elif rechk[0] == "ula":
		if os.access(str(rechk[1]), os.F_OK):
			print "\033[32m*\033[0m File exists"
			ulfile = open(str(rechk[1]), "rb")
		        print "\033[32m*\033[0m [ASCII Mode]Uploading: "+str(rechk[1])+"..."
			ftpsrv.storlines('STOR '+str(rechk[1]), ulfile)
			print "\033[32m*\033[0m Uploaded file "+"'"+str(rechk[1])+"'"+" which size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
			raw_input("Press any key to get back")
		else:
			print "\033[31m*\033[0m Your file doesn't exists"
			raw_input("Press any key to get back")

	#Help page
	elif prompt == 'h':
		print "FTPH Browser Commands: "
		print "***This page is under construction***"
		raw_input("Press any key to get back...")

	#If no command matches
	else:
		pass

#Mainf, all start here
def mainf():
	connect(arg_url_ftp, debuglevel)
	login(arg_url_ftp)
	ftpWelcome(arg_url_ftp, username)

##Hello! :D##
if __name__ == '__main__':
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
else:
	print "\n"
	sys.exit(1)
