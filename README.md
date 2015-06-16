# ftp-handler
==============

This is FTP-Handler, a simple and lightweight manager for your FTPs.

==============

# How to use?

Easier than ever: run
*./install.sh*
and then
*ftph*

# This project is under development

 We expect to implement 
 
 - SSL Support
 - A favourite list to easy access your FTP favourite server
 - GUI (PyGTK -- TkInter)

# Hope you will give it a try! :P 

*No licence, be free to fork this repo*

#*Changelog*

 [*2015/06/14*]

 - Init :)
 
 [*2015/06/15*]

 - Arguments (syntax: *ftph url debuglevel* , use --help to get help)
 - defined mainf() [all start here]
 - defined login() [after connect()]
 - defined connect() [gets the argument and it will try to reach the *url* ]
 
 [*2015/06/17*]
 
 - Added Welcome message
 - Added FTP command prompt
 - Listing directory
 - nslookup (socket module)
 - more...


