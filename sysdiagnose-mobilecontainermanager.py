#! /usr/bin/env python

# For Python3
# Script to print uninstall infor from logs/MobileContainerManager/containermanagerd.log.0
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser

version_string = "sysdiagnose-mobilecontainermanager.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/MobileContainerManager/containermanagerd.log.0 To Be Searched")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

linecount = 0
hitcount = 0
with open(options.inputfile, 'r') as fp:
    data = fp.readlines()

    for line in data:
        linecount += 1
        
        if '[MCMGroupManager _removeGroupContainersIfNeededforUser:groupContainerClass:identifiers:referenceCounts:]: Last reference to group container' in line:
            hitcount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            group = txts[15]
            print(day + " " + month + " " + year + " " + time + " Removed " + group + " [line " + str(linecount) + "]")
    
print("\nFound " + str(hitcount) + " group removal entries\n")



