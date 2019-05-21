#! /usr/bin/env python

# For Python3
# Script to print the values from logs/Networking/com.apple.networkextension.cache.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

#import pprint

version_string = "sysdiagnose-net-ext-cache.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)


usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/Networking/com.apple.networkextension.cache.plist To Be Searched")
parser.add_option("-v", dest="verbose",
                  action="store_true", default=False,
                  help="Print GUIDs as well as app names")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

print("Running " + version_string + "\n")

count = 0
with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
    #pprint.pprint(pl)
    #print(pl.keys())

    if 'app-rules' in pl.keys():
        for key, list1 in pl["app-rules"].items():
            count += 1
            if (options.verbose):
                print(str(key) + " = " + ', '.join(list1)) # verbose with GUIDs
            else:
                print(str(key)) # just app names

    print("\n" + str(count) + " cache entries retrieved\n")



