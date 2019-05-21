#! /usr/bin/env python

# For Python3
# Script to print the values from logs/MobileBackup/com.apple.MobileBackup.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

#import pprint

version_string = "sysdiagnose-mobilebackup.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)


usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/MobileBackup/com.apple.MobileBackup.plist To Be Searched")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

print("Running " + version_string + "\n")

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
    #pprint.pprint(pl)
    #print(pl.keys())

    if 'BackupStateInfo' in pl.keys():
        for key, val in pl["BackupStateInfo"].items():
            #print("key = " + str(key) + ", val = " + str(val))
            if key == 'date':
                print("BackupStateInfo Date = " + str(val))
            if key == 'isCloud':
                print("BackupStateInfo isCloud = " + str(val))
                
    if 'RestoreInfo' in pl.keys():
        for key, val in pl["RestoreInfo"].items():
            if key == 'RestoreDate':
                print("RestoreInfo Date = " + str(val))
            if key == 'BackupBuildVersion':
                print("RestoreInfo BackupBuildVersion = " + str(val))
            if key == 'DeviceBuildVersion':
                print("RestoreInfo DeviceBuildVersion = " + str(val))
            if key == 'WasCloudRestore':
                print("RestoreInfo WasCloudRestore = " + str(val))  
                
                
