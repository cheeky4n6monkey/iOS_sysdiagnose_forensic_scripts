#! /usr/bin/env python

# For Python3
# Script to print the values from /logs/SystemVersion/SystemVersion.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

version_string = "sysdiagnose-sys.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="/logs/SystemVersion/SystemVersion.plist To Be Searched")
(options, args) = parser.parse_args()

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
print("ProductName = " + pl["ProductName"])
print("ProductVersion = " + pl["ProductVersion"])
print("ProductBuildVersion = " + pl["ProductBuildVersion"])



