#! /usr/bin/env python2.7 
# -*- coding: utf-8 -*-

# FtpH : A Command Line Interface handler for your FTPs
# 
# Git Repository: github.com/StefanoBelli/ftp-handler
# 
# To get latest releases:
# execute - git pull in ftp-handler/ local repository
#
# { Version: 1.0 }
# { Update Date: DD/MM/YYYY - 20/06/2015 } 
# { Status: [WORKING] } 
#
# Developer(s):
#  ---> StefanoBelli
#  \____mailto: <stefano9913@gmail.com>
#   \___GooglePlus: <plus.google.com/+StefanoBelli>
#    \__Website : <http://inthebit.it>
#
# to get latest update, go to ftp-handler/ local directory and execute 'git pull' inside this directory :)
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
from socket import error
from ftplib import error_reply
from ftplib import all_errors
from ftplib import error_proto

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
version = float(1.0) 
udate = "20/06/2015"

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
FTPH: FTP Handler
++++++++++++++++++
Usage: \033[33m[./ftph.py]\033[0m \033[34m<url/help>\033[0m \033[31m(debug level)\033[0m
++++++++++++++++++
\033[34murl/help\033[0m: Type ftp server URL (like this: ftp.site.com) / --help, to type this help page.
\033[31mdebug level\033[0m: Defines how many debug messages the FTP server should show. It is not compulsory, see below.
\033[33m***WARNING: TO SEE HOW TO USE FTPH BROWSER, TYPE COMMAND 'h' (to see how to use other commands) WHEN YOU GET INTO THE FTP Browser***\033[0m
++++++++++++++++++
Debug Values: (integer)
->\033[32m1\033[0m : minimum debug level
->\033[33m2\033[0m : higher debug level
If you don't declare any debug level, the value is \033[34m0\033[0m
++++++++++++++++++
Usage Example: 
\033[33mftph\033[0m \033[34mftp.debian.org\033[0m   (Debug level will be null)
\033[33mftph\033[0m \033[34mftp.debian.org\033[0m \033[31m1\033[0m (Debug level will be min)
\033[33mftph\033[0m \033[34mftp.debian.org\033[0m \033[31m2\033[0m (Debug level will be max)
++++++++++++++++++
Developer: 
Stefano Belli
\_-> GitHub: <https://github.com/StefanoBelli>
 \_-> Google+: <https://plus.google.com/+StefanoBelli>
  \_-> mailto: <stefano9913@gmail.com>
   \_-> Website: <http://www.inthebit.it>
+++++++++++++++++++
GitHub FTPH Repository: \033[32m<https://github.com/StefanoBelli/ftp-handler>\033[0m
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
        except error:
                print "\033[31m * \033[0m Connection refused by %s !!"%url
                sys.exit(3)
	print "\033[32m * \033[0m Succesfully connected to %s - [IP: %s] \n"%(url, getsrvip)
	sleep(1)

#Login to the connected server
def login(strurl):
	try:
		global username
		print "************LOGIN @ %s**********************************************************" %strurl
		print "\033[34m===To connect anonymously, leave empty username and password                 "
		print "===But remember that if you login as anonymous you can't do something        "
		print "===Such as copy, delete, rename files/directory, upload files.               "
		print "===And some servers don't accept Anonymous users.\033[0m                            "
                print "" 
		print "\033[33m!=Password is NOT shown=!\033[0m"
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
        print "\033[32m*\033[0m Logged-In from: %s:%s:%s on %s/%s/%s" %(lgtime.tm_hour, lgtime.tm_min, lgtime.tm_sec, lgtime.tm_year, lgtime.tm_mon, lgtime.tm_mday)
	print "\033[32m*\033[0m"
	print "\033[32m+-----~Welcome to~[\033[0m\033[34m%s\033[0m\033[32m]~that says-----------+\033[0m" %strurl 
	print ftpsrv.getwelcome()
	print "\033[32m+---------~~~[\033[0mIP:\033[34m%s\033[0m\033[32m]~~~--------------------+\033[0m" %getsrvip
	prompt(srvuser)
	return srvuser

#Prompt (FTP Browser prompt)
def prompt(suser):
        try:
	    dirr = ftpsrv.nlst()
        except error_perm:
                print "\033[31m * \033[0m No files/directory were found on this FTP!"
                if suser == "anonymous user":
                       print "\033[33m * \033[0mClosing Connection..."
                       ftpsrv.quit()
                       print "\033[32m * \033[0mBye bye!"
                       sys.exit(1)
                else:
                       print "\033[33m * \033[0mClosing connection..."
                       ftpsrv.quit()
                       print "\033[32m * \033[0mBye bye!"
                       sys.exit(1)
	print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip)
	print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
	for i in range(len(dirr)):
		print "\033[34m>>>\033[0m "+str(dirr[i])
	print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
        print "\033[31m*****\033[0m Use command 'h' to get help about explore the FTP\033[31m *****\033[0m" 
	print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip) 
	prompt = raw_input("\033[32m>>>\033[0m ")
        try:
	    checkPrompt(prompt)
        except error_reply:
            print "\033[33m * \033[0m Unexpected reply from server!!"
            sleep(1)
            pass
        except IndexError:
            print "\033[32m * \033[0m If you are seeing this message, maybe you didn't type all asked arguments, use command 'h' to see more"
            raw_input("Press [enter] to get back")
            pass
	while (prompt != "ex"):
		os.system("clear")
		dirr = ftpsrv.nlst()
		print ""
		print "\033[32m*\033[0m Logged in from: %s:%s:%s on %s/%s/%s" %(lgtime.tm_hour, lgtime.tm_min, lgtime.tm_sec, lgtime.tm_year, lgtime.tm_mon, lgtime.tm_mday)
		print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip)
		print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
		for i in range(len(dirr)):
			print "\033[34m>>>\033[0m "+str(dirr[i])
		print "\033[32mCurrent Working Directory\033[0m: \033[34m%s\033[0m" %ftpsrv.pwd()
		print "=\033[33mDIRECTORY\033[0m-----[\033[34m%s\033[0m]-[\033[34m%s\033[0m]================================================"%(suser, getsrvip) 
		prompt = raw_input("\033[32m>>>\033[0m ")
                try:
		    checkPrompt(prompt)
                except error_reply:
                    print "\033[33m * \033[0m Unexpected reply from server!!"
                    sleep(1)
                    pass
                except IndexError:
                    print "\033[31m * \033[0m If you are seeing this message, maybe you didn't type all asked argument, use command 'h' to see more." 
                    raw_input("Press [enter] to get back")
                    pass 

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
                try:
		    ftpsrv.rmd(str(rechk[1]))
                except error_perm:
                    print "\033[31m * \033[0m You can't remove directory! (Not allowed)"
                    raw_input("Press [enter] to get back")
                    pass

	#RemoveFile command
	elif rechk[0] == "rf":
                try:
		    ftpsrv.delete(str(rechk[1]))
                except error_perm:
                    print "\033[31m * \033[0m You can't remove files! (Not allowed)"
                    raw_input("Press [enter] to get back")
                    pass

	#Size of file command
	elif rechk[0] == "sz":
		fsize = ftpsrv.size(str(rechk[1]))
		print "File %s is big: %s Byte(s)" %(str(rechk[1]), str(fsize))
		raw_input("Press [enter] to get back")

	#Make Directory command
	elif rechk[0] == "md":
                try:
		    ftpsrv.mkd(str(rechk[1]))
                except error_perm:
                    print "\033[31m * \033[0m You can't make directories! (Not allowed)"
                    raw_input("Press [enter] to get back")
                    pass
	
	#Rename File & Directories 
	elif rechk[0] == "rn":
                try:
		    ftpsrv.rename(str(rechk[1]), str(rechk[2]))
                except error_perm:
                    print "\033[31m * \033[0m You can't rename files / directories! (Not allowed) "
                    raw_input("Press [enter] to get back")
                    pass
	
	#List directories
	elif rechk[0] == "als":
		dirname = str(rechk[1])
		print "*-*-*-*-*\033[34mListing directory: %s\033[0m*-*-*-*-*" %dirname
		ftpsrv.dir(dirname)
		raw_input("Press [enter] to get back")

	#Get Binary file (non ASCII) from FTP
	elif rechk[0] == "dlb":
		dlfile = open(str(rechk[2]), "wb").write
		print "\033[32m*\033[0m Downloading: "+str(rechk[1])+"..."
		print "\033[33m*\033[0m Requested file "+"'"+str(rechk[1])+"'"+" size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
		ftpsrv.retrbinary("RETR "+str(rechk[1]), dlfile)
		print "\033[32m*\033[0m Downloaded file: "+os.getcwd()+"/"+rechk[2]
		raw_input("Press [enter] to get back")

	#Upload Binary file (non ASCII) to FTP
	elif rechk[0] == "ulb":
		if os.access(str(rechk[1]), os.F_OK):
                        try:
			    print "\033[32m*\033[0m File exists"
			    ulfile = open(str(rechk[1]), "rb")
		            print "\033[32m*\033[0m Uploading: "+str(rechk[1])+"..."
			    ftpsrv.storbinary('STOR '+str(rechk[1]), ulfile)
			    print "\033[32m*\033[0m Uploaded file "+"'"+str(rechk[1])+"'"+" which size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
			    raw_input("Press [enter] to get back")
                        except error_perm:
                            print "\033[31m * \033[0m You can't upload files! (Not allowed)"
                            raw_input("Press [enter] to get back")
                            pass
		else:
			print "\033[31m*\033[0m Your file doesn't exists"
			raw_input("Press [enter] to get back")
                        pass

	#Get ASCII Lines from FTP
	elif rechk[0] == "dla":
		dlfile = open(str(rechk[2]), "wb").write
		print "\033[32m*\033[0m [ASCII Mode]Downloading: "+str(rechk[1])+"..."
		print "\033[33m*\033[0m Requested file "+"'"+str(rechk[1])+"'"+" size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
		ftpsrv.retrlines("RETR "+str(rechk[1]), dlfile)
		print "\033[32m*\033[0m Downloaded file: "+os.getcwd()+"/"+rechk[2]
		raw_input("Press [enter] to get back")

	#Upload ASCII Lines to FTP
	elif rechk[0] == "ula":
		if os.access(str(rechk[1]), os.F_OK):
                        try:
			    print "\033[32m*\033[0m File exists"
			    ulfile = open(str(rechk[1]), "rb")
		            print "\033[32m*\033[0m [ASCII Mode]Uploading: "+str(rechk[1])+"..."
			    ftpsrv.storlines('STOR '+str(rechk[1]), ulfile)
			    print "\033[32m*\033[0m Uploaded file "+"'"+str(rechk[1])+"'"+" which size is: "+str(ftpsrv.size(str(rechk[1])))+" Byte(s)"
			    raw_input("Press [enter] to get back")
                        except error_perm:
                            print "\033[31m * \033[0m You can't upload files! (Not allowed)"
                            raw_input("Press [enter] to get back")
                            pass 
		else:
			print "\033[31m*\033[0m Your file doesn't exists"
			raw_input("Press [enter] to get back")
                        pass
        #FTP Command
        elif rechk[0] == "fcmd":
                try:
                    rechk.pop(0)
                    cmdStr = " ".join(rechk)
                    print "FTP Command: "+str(cmdStr)
                    ftpsrv.sendcmd(cmdStr)
                    raw_input("Press [enter] to get back")
                except error_perm:
                    print "\033[31m * \033[0m This command wasn't recognized"
                    raw_input("Press [enter] to get back")
                except error_temp:
                    print "\033[31m * \033[0m Refused."
                    raw_input("Press [enter] to get back")
                except EOFError:
                    pass

	#Help page
	elif prompt == 'h':
                help_page_browser = '''
                This is the FTPH Browser commands help page 
                +-----------------------------------------+
                Syntax: \033[32m<command>\033[0m \033[33m[argument]\033[0m \033[34m(other arg)\033[0m
                Keep 1 space between command and argument always!
                +-----------------------------------------+
                |Commands|
                +-----------------------------------------+
                \033[33m** NOTE THAT IF YOU LOGIN AS ANONYMOUS YOU CAN'T DO MANY THINGS**\033[0m
                \033[32m==>\033[0m Explore the server:
                ===========================================
                \033[32mcd\033[0m: Changes Directory
                \033[32mals\033[0m: List directory with more details
                \033[32msz\033[0m: Checks the size of a file on the server
                ===========================================
                *Example:
                ++cd directory
                ++als directory/anotherdir
                ++sz myfile 

                \033[32m==>\033[0m Commands that launches commands
                ===========================================
                \033[32mfcmd\033[0m : Launches an FTP Command 
                \033[32mosh\033[0m : Launches a local shell (/bin/sh)
                \033[32mex\033[0m : Closes connection and exits the program
                ===========================================
                *Example:
                ++fcmd RETR something
                ++osh
                ++ex

                \033[32m==>\033[0m Modify files, directory, creating, deleting, renaming
                ===========================================
                \033[32mrn\033[0m : renames a directory/file
                \033[32mmd\033[0m : makes a directory
                \033[32mrd\033[0m : removes a directory
                \033[32mrf\033[0m : removes a file
                ===========================================
                *Example:
                ++rn rename_me to_this
                ++md make_this_directory
                ++rd remove_this_diretory
                ++rf remove_this_file

                \033[32m==>\033[0m Downloading and uploading files
                ===========================================
                \033[32mdlb\033[0m : Downloads a file in binary mode (search the web to see the difference between binary and ASCII mode)
                \033[32mdla\033[0m : Downloads a file in ASCII mode 
                \033[32mulb\033[0m : Uploads a file in binary mode
                \033[32mula\033[0m : Uploads a file in ASCII mode
                ===========================================
                *Example:
                ++dlb SERVER_FILE SAVE_HERE (You the second argument is the destination name file on your local enviornment)
                ++dla SERVER_FILE SAVE_HERE (same as above)
                ++ulb MYFILE
                ++ula MYFILE

                ALWAYS KEEP 1 SPACE BETWEEN COMMANDS AND ARGUMENTS
                '''

                os.system("clear")
                print help_page_browser
		raw_input("Press [enter] get back...")

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
        except IOError:
                print "\033[34m * \033[0mInput / Output error!"
                sys.exit(1)
	except SyntaxError:
		print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Syntax] mistake, not yours! :) \n"
		sys.exit(1)
	except TypeError:
		print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Type, var] mistake, not yours! :) \n"
	        sys.exit(1)
	except AttributeError:
		print "\n\033[31m * \033[0mDon't worry if you see this message, this is a developer [Attribute] mistake, not yours! :) \n"
          	sys.exit(1)
        except all_errors:
                print "\033[31m * \033[0mUnhandled [FTP] error! This exception was raised to avoid ugly messages, so I don't know what the problem was! :/"
                pass
        except error_proto:
                pass
else:
	print "\n"
	sys.exit(1)
