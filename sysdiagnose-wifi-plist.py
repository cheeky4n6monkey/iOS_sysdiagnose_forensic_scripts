#! /usr/bin/env python

# For Python3
# Script to print the values from WiFi/com.apple.wifi.plist or WiFi/preferences.plist
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import plistlib

#import pprint

version_string = "sysdiagnose-wifi-plist.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)


usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="WiFi/com.apple.wifi.plist or WiFi/preferences.plist To Be Searched")
parser.add_option("-t", dest="outputtsv",
                  action="store_true", default=False,
                  help="Write TSV output file called sysdiagnose-wifi-plist-output.TSV")                  
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

print("Running " + version_string + "\n")

outputlist = []
with open(options.inputfile, 'rb', ) as fp:
    pl = plistlib.load(fp)
    #pprint.pprint(pl)
    #print(pl.keys())

    if 'List of known networks' in pl.keys():
        for dic in pl['List of known networks']: # list of dicts
            #print(item)
            print("=============================")
            print("SSID_STR = " + dic['SSID_STR'])
            ssid = dic['SSID_STR']
            bssid = ""
            if 'BSSID' in dic.keys():
                print("BSSID = " + dic['BSSID'])
                bssid = dic['BSSID']
            
            netusage = ""    
            if 'networkUsage' in dic.keys():
                print("networkUsage = " + str(dic['networkUsage']))               
                netusage = str(dic['networkUsage'])
           
            countrycode = ""
            if '80211D_IE' in dic.keys():
                #print(type(dic['80211D_IE'])) # dict
                for key2, val2 in dic['80211D_IE'].items():
                    if key2 == 'IE_KEY_80211D_COUNTRY_CODE':
                        print("IE_KEY_80211D_COUNTRY_CODE = " + val2)
                        countrycode = val2

            devname = ""
            mfr = ""
            serialnum = ""
            modelname = ""
            if 'WPS_PROB_RESP_IE' in dic.keys():
                for key3, val3 in dic['WPS_PROB_RESP_IE'].items():
                    
                    if key3 == 'IE_KEY_WPS_DEV_NAME':
                        print("IE_KEY_WPS_DEV_NAME = " + val3)
                        devname = val3
                    if key3 == 'IE_KEY_WPS_MANUFACTURER':
                        print("IE_KEY_WPS_MANUFACTURER = " + val3)
                        mfr = val3
                    if key3 == 'IE_KEY_WPS_SERIAL_NUM':
                        print("IE_KEY_WPS_SERIAL_NUM = " + val3)
                        serialnum = val3
                        #serialnum = "testserial"
                    if key3 == 'IE_KEY_WPS_MODEL_NAME':
                        print("IE_KEY_WPS_MODEL_NAME = " + val3)
                        modelname = val3
                        #modelname = "testmodel"
            
            lastjoined = ""    
            if 'lastJoined' in dic.keys():
                print("lastJoined = " + str(dic['lastJoined']))
                lastjoined = str(dic['lastJoined'])
            lastautojoined = ""
            if 'lastAutoJoined' in dic.keys():    
                print("lastAutoJoined = " + str(dic['lastAutoJoined']))
                lastautojoined = str(dic['lastAutoJoined'])
            if 'enabled' in dic.keys():
                enabled = str(dic['enabled'])    
                print("enabled = " + str(dic['enabled']))
            print("=============================\n")
            
            outputlist.append((ssid, bssid, netusage, countrycode, devname, mfr, serialnum, modelname, lastjoined, lastautojoined, enabled))


if (options.outputtsv):                
    with open("sysdiagnose-wifi-plist-output.TSV", 'w') as wp:
        wp.write("SSID\tBSSID\tNETUSAGE\tCOUNTRYCODE\tDEVICENAME\tMANUFACTURER\tSERIALNUM\tMODELNAME\tLASTJOINED\tLASTAUTOJOINED\tENABLED\n") # header
        for ssid, bssid, netusage, countrycode, devname, mfr, serialnum, modelname, lastjoined, lastautojoined, enabled in outputlist:
            wp.write(ssid+"\t"+bssid+"\t"+netusage+"\t"+countrycode+"\t"+devname+"\t"+mfr+"\t"+serialnum+"\t"+modelname+"\t"+lastjoined+"\t"+lastautojoined+"\t"+enabled+"\n")
    
    print("Also outputted to sysdiagnose-wifi-plist-output.TSV\n")

