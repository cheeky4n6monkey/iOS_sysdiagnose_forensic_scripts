#! /usr/bin/env python

# For Python3
# Script to print the values from /logs/Networking/preferences.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

version_string = "sysdiagnose-networkprefs.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="/logs/Networking/preferences.plist To Be Searched")
(options, args) = parser.parse_args()

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
#print(pl.keys()) # dict_keys(['CurrentSet', 'System', 'Sets', 'NetworkServices'])

if 'System' in pl.keys():
    #print(pl["System"])
    #print(type(pl["System"])) = dict
    if 'System' in pl["System"].keys():
        for key, val in pl["System"].items():
            if key == 'System': 
                print("System ComputerName = " + val["ComputerName"]) # System/System/ComputerName
                print("System HostName = " + val["HostName"]) # System/System/HostName
            if key == 'Network':
                for key2, val2 in val["HostNames"].items():
                    print("Network LocalHostName = " + val2) # for each System/Network/HostNames/LocalHostName





