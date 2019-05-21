#! /usr/bin/env python

# For Python3
# Script to print the values from logs/Networking/NetworkInterfaces.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

version_string = "sysdiagnose-networkinterfaces.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/Networking/NetworkInterfaces.plist To Be Searched")
(options, args) = parser.parse_args()

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
    if 'Interfaces' in pl.keys():
        #print(pl["Interfaces"])
        #print(type(pl["Interfaces"])) = dict
        
        for dictn in pl['Interfaces']:
            print("==================================")
            print("BSD Name = " + dictn['BSD Name'])
            if 'Active' in dictn.keys():
                print("Active = " + str(dictn['Active']))
            #print("IOMACAddress = " + str(dictn['IOMACAddress'])) # dictn['IOMACAddress'] = bytes type
            print("IOMACAddress = " + dictn['IOMACAddress'].hex()) # string type
            print("IOPathMatch = " + dictn['IOPathMatch'])
            
            for key, val in dictn['SCNetworkInterfaceInfo'].items():
                if key == 'UserDefinedName':
                    print("UserDefinedName = " + val)
        


