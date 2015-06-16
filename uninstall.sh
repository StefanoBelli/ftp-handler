#! /bin/sh
# Uninstaller for ftph

checkIfPresent(){
	[[ -f /usr/bin/ftph ]] && echo "" || exit 2
}

if [[ $USER == "root" ]]; then
	checkIfPresent
	printf "\033[33m*\033[0m Deleting ftph...\n"
	rm /usr/bin/ftph && 
	printf "\033[32m*\033[0m Done.\n"
	exit 0 || 
	printf "\033[31m*\033[0m There was a problem!\n"
	exit 1
else
	printf "\033[31m*\033[0m You need to be root!\n"
	exit 2
fi
