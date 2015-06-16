#!/bin/sh

checkForOld()
{
	[[ -f /usr/bin/ftph ]] &&
		printf "\033[33m*\033[0m ftph already present.... Overwriting\n" ||
		echo ""
}

if [[ $USER == "root" ]]; then
	checkForOld
	printf "\033[32m*\033[0m Copying...\n"
	cp src/ftp-handler.py /usr/bin/ftph 
	printf "\033[32m*\033[0m Changing execution mode...\n"
	chmod +x /usr/bin/ftph && 
	printf "\033[32m*\033[0m Done.\nNow just execute ftph :)\n"
	exit 0 ||
	printf "\033[31m*\033[0m There was a problem.\n"
	exit 1
else
	printf "\033[31m*\033[0m You need to be root, nothing to do.\n"
	exit 1
fi
