#! /usr/bin/env python

# For Python3
# Script to print Mobile Activation Startup and Upgrade info from logs/MobileActivation/mobileactivationd.log.*
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser

version_string = "sysdiagnose-mobileactivation.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/MobileActivation/mobileactivationd.log.* To Be Searched")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

linecount = 0
hitcount = 0
activationcount = 0
with open(options.inputfile, 'r') as fp:
    data = fp.readlines()

    for line in data:
        linecount += 1
        
        if 'perform_data_migration' in line:
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
            frombuild = txts[12]
            tobuild = txts[14]
            print("\n" + day + " " + month + " " + year + " " + time + " Upgraded from " + frombuild + " to " + tobuild + " [line " + str(linecount) + "]")
    
    
        if 'MA: main: ____________________ Mobile Activation Startup _____________________' in line:
            activationcount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            print("\n" + day + " " + month + " " + year + " " + time + " Mobile Activation Startup " + " [line " + str(linecount) + "]")
            
        if 'MA: main: build_version:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            buildver = txts[11]
            print(day + " " + month + " " + year + " " + time + " Mobile Activation Build Version = " + buildver)
            
        if 'MA: main: hardware_model:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            hwmodel = txts[11]
            print(day + " " + month + " " + year + " " + time + " Mobile Activation Hardware Model = " + hwmodel)
            
        if 'MA: main: product_type:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            prod = txts[11]
            print(day + " " + month + " " + year + " " + time + " Mobile Activation Product Type = " + prod)
            
        if 'MA: main: device_class:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            dayofweek = txts[0]
            month = txts[1]
            day = txts[2]
            time = txts[3]
            year = txts[4]
            devclass = txts[11]
            print(day + " " + month + " " + year + " " + time + " Mobile Activation Device Class = " + devclass)
            
print("\nFound " + str(hitcount) + " Upgrade entries")

print("Found " + str(activationcount) + " Mobile Activation Startup entries\n")

