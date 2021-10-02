#!/usr/bin/python3.6
import os, sys, hashlib
from shutil import copy
''' Python version of bash code below '''
class calc():
    def __init__(self):
        self.recur = 0 # set counter to null
        self.newpath = sys.argv[1] # get first argument
        self.oldpath = sys.argv[2] # get second argument
        self.oldhash = hashlib.md5(open(self.oldpath, 'rb').read()).hexdigest() #check hash
        self.newhash = hashlib.md5(open(self.newpath, 'rb').read()).hexdigest() #check hash
        if self.oldhash != self.newhash: #compare hash
            self.main() #if hash isnt similar. Do a copy.
    def main(self):
        '''copy'''
        if copy(self.oldpath, self.newpath): # Copy
            ''' double check that the file was copied correctly, otherwise call self.'''
            if self.oldhash != hashlib.md5(open(self.newpath, 'rb').read()).hexdigest(): #check old hash against new hash
                self.recur += 1 # add 1 to counter
                if self.recur < 2: # if counter has is larger than 3
                    return('Unable to correct erroneus copy.')       #return this
                self.main() # otherwise do the copy operation again
            return('Corrected erroneus copy.') # when done, return success.
calc() # run code.

# !/bin/bash
# source /drive/drive/.rtorrent/scripts/master.sh
# _script="sickrage_postproc.sh"
# oldpath="$2" 
# newpath="$1" 
# if [ "$(crc32 "$oldpath")" = "$(crc32 "$newpath")" ]; then
# 	log n "${newpath##*/} copied correctly by Medusa"
# else
# 	if [ "$newpath" != "/" ]; then 	#lets not make any mistakes
# 		rm -rf "$newpath"	#remove botched copy
# 		log s "${newpath##*/} copied incorrectly, correcting Medusas mistake"
# 		cp -r "$oldpath" "$newpath":q
# 	fi
# fi