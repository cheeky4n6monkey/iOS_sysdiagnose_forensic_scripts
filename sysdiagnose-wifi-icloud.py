#! /usr/bin/env python

# For Python3
# Script to print the values from WiFi/ICLOUD_com.apple.wifid.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

version_string = "sysdiagnose-wifi-icloud.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="WiFi/ICLOUD_com.apple.wifid.plist To Be Searched")
parser.add_option("-t", dest="outputtsv",
                  action="store_true", default=False,
                  help="Write TSV output file called sysdiagnose-wifi-icloud-output.TSV")  
(options, args) = parser.parse_args()

netlist = []

with open(options.inputfile, 'rb') as fp:
    pl = plistlib.load(fp)
    if 'values' in pl.keys():
        name = ""
        timestamp =""
        bssid = ""
        ssid = ""
        addedat = ""
        addedby = ""
        enabled = ""
        for key, val in pl['values'].items(): # values contains an entry for each wifi net
            print("==================================")
            print("Name = " + key)
            name = key
            
            if type(val) == dict:
                for key2, val2 in val.items():
                    if key2 == 'timestamp':
                        print("timestamp = " + str(val2))
                        timestamp = str(val2)
                        
                    if key2 == 'value':
                        if type(val2) == dict:
                            for key3, val3 in val2.items():
                                if key3 == 'BSSID':
                                    print("BSSID = " + str(val3))
                                    bssid = str(val3)
                                if key3 == 'SSID_STR':
                                    print("SSID_STR = " + str(val3))
                                    ssid = str(val3)
                                if key3 == 'added_at':
                                    print("added_at = " + str(val3))
                                    addedat = str(val3)
                                if key3 == 'added_by':
                                    print("added_by = " + str(val3))
                                    addedby = str(val3)
                                if key3 == 'enabled':
                                    print("enabled = " + str(val3))
                                    enabled = str(val3)
            
            netlist.append((name, timestamp, bssid, ssid, addedat, addedby, enabled))
                                    
        print("\nRetrieved " + str(len(pl['values'].keys())) + " wifi entries\n")


if (options.outputtsv):                
    with open("sysdiagnose-wifi-icloud-output.TSV", 'w') as wp:
        wp.write("NAME\tTIMESTAMP\tBSSID\tSSID\tADDEDAT\tADDEDBY\tENABLED\n") # header
        for name, timestamp, bssid, ssid, addedat, addedby, enabled in netlist:
            wp.write(name+"\t"+timestamp+"\t"+bssid+"\t"+ssid+"\t"+addedat+"\t"+addedby+"\t"+enabled+"\n")
    
    print("Also outputted to sysdiagnose-wifi-icloud-output.TSV\n")
    
    

