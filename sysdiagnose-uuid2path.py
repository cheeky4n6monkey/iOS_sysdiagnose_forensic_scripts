#! /usr/bin/env python

# For Python3
# Script to print the values from logs/tailspindb/UUIDToBinaryLocations (XML plist)
# Uses Python3's plistlib
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib
import pprint

version_string = "sysdiagnose-uuid2path.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/tailspindb/UUIDToBinaryLocations plist To Be Printed")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

print("Running " + version_string + "\n")

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
    for key, val in pl.items():
        print(str(key) + ", " + str(val))

    print("\n" + str(len(pl.keys())) + " GUIDs found\n")



