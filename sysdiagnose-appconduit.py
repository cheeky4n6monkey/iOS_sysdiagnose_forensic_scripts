#! /usr/bin/env python

# For Python3
# Script to print connection info from logs/AppConduit/AppConduit.log.*
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser

version_string = "sysdiagnose-appconduit.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/AppConduit/AppConduit.log.* To Be Searched")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

linecount = 0
connectedcount = 0
resumecount = 0
reunioncount = 0
disconnectedcount = 0
suspendcount = 0

with open(options.inputfile, 'r') as fp:
    data = fp.readlines()

    for line in data:
        linecount += 1
        
        if '[ACXCompanionSyncConnectionManager devicesAreNowConnected:]: Device' in line:
            connectedcount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if(len(txts) > 10):
                dayofweek = txts[0]
                month = txts[1]
                day = txts[2]
                time = txts[3]
                year = txts[4]
                device = txts[11]
                print(day + " " + month + " " + year + " " + time + " - " + device + " Now Connected [line " + str(linecount) + "]")
            else:
                #malformed message ... ignore
                print("\nMalformed devicesAreNowConnected entry at line "+str(linecount)+"\n")
                
    
        if '[ACXInstallQueue reachabilityChangedForDevice:]_block_invoke: Resuming because' in line:
            resumecount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if(len(txts) > 11):
                dayofweek = txts[0]
                month = txts[1]
                day = txts[2]
                time = txts[3]
                year = txts[4]
                device = txts[12]
                print(day + " " + month + " " + year + " " + time + " - " + device + " Resuming [line " + str(linecount) + "]")
            else:
                #malformed message ... ignore
                print("\nMalformed Resuming entry at line "+str(linecount)+"\n")

         
        if '[ACXCompanionSyncConnection performReunionSyncWithReason:]_block_invoke: Starting reunion sync because ' in line:
            reunioncount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if(len(txts) > 14):
                dayofweek = txts[0]
                month = txts[1]
                day = txts[2]
                time = txts[3]
                year = txts[4]
                buildver = txts[15]
                print(day + " " + month + " " + year + " " + time + " - " + device + " Starting Reunion Sync [line " + str(linecount) + "]")
            else:
                #malformed message ... ignore
                print("\nMalformed Sync entry at line "+str(linecount)+"\n")
                
            
        if '[ACXCompanionSyncConnectionManager devicesAreNoLongerConnected:]: Device' in line:
            disconnectedcount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if(len(txts) > 10):
                dayofweek = txts[0]
                month = txts[1]
                day = txts[2]
                time = txts[3]
                year = txts[4]
                device = txts[11]
                print(day + " " + month + " " + year + " " + time + " - " + device + " Disconnected [line " + str(linecount) + "]")
            else:
                #malformed message ... ignore
                print("\nMalformed devicesAreNoLongerConnected entry at line "+str(linecount)+"\n")
            
        if '[ACXInstallQueue reachabilityChangedForDevice:]_block_invoke: Suspending because' in line:
            suspendcount += 1
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if(len(txts) > 11):
                dayofweek = txts[0]
                month = txts[1]
                day = txts[2]
                time = txts[3]
                year = txts[4]
                device = txts[12]
                print(day + " " + month + " " + year + " " + time + " - " + device + " Suspending [line " + str(linecount) + "]")
            else:
                #malformed message ... ignore
                print("\nMalformed Suspending entry at line "+str(linecount)+"\n")
            
            
print("\nFound " + str(connectedcount) + " Now Connected entries")
print("Found " + str(resumecount) + " Resuming entries")
print("Found " + str(reunioncount) + " Starting Reunion Sync entries")
print("Found " + str(disconnectedcount) + " Disconnected entries")
print("Found " + str(suspendcount) + " Suspending entries\n")



