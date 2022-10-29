#! /usr/bin/env python

# For Python3
# Script to print the Network names (and log to TSV) from WiFi/wifi*.log
# Author: cheeky4n6monkey@gmail.com

import sys
from optparse import OptionParser
import tarfile
import re
import shlex

version_string = "sysdiagnose-wifi-net.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="WiFi/wifi*.log To Be Searched")
(options, args) = parser.parse_args()

linecount = 0
ignorecount = 0
filterednetworkscount = 0
channelsfoundcount = 0
backgroundscancount = 0
MRUnetworkscount = 0
ppmattachedcount = 0
alreadyattachedcount = 0

filterednetworks = []
channelsfound = []
backgroundscan = []
MRUnetworks = []
ppmattached = []
alreadyattached = []

#print(options.inputfile[0:-4]) # = wifi-buf-04-26-2019__16:00:52.768.log

if options.inputfile.endswith('.tgz'): # eg wifi-buf-04-26-2019__16:00:52.768.log.tgz
    # untar file first to current directory
    # tarfile.open Throws InvalidHeader error!
    with tarfile.open(options.inputfile, 'r:gz') as t:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(t, "./")
    # does not get here due to exception ... todo
   
    # readfile = ass-ume extracted name is same as input name minus the .tgz
    with open(options.inputfile[0:-4], 'r') as fp:
         data = fp.readlines()
    # TODO: Implement processing when given zip file
        
else: # ass-ume input file has been untarred already and is plaintext
    with open(options.inputfile, 'r') as fp:
         data = fp.readlines()

    for line in data:
        linecount += 1
        
        if 'AJScan: Filtered networks -' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 7: # 7th field is first network name (after "AJScan: Filtered networks -")
                    filterednetworkscount += 1
                    date = txts[0]
                    time = txts[1]
                    networks = txts[7:-1] # skip last item "..."
                    #print("$$$ Filtered Networks found = " + ' '.join(networks) + ", line = " + str(linecount))
                    for net in networks: # each network gets own entry
                        filterednetworks.append((date, time, net, linecount))    
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Filtered Networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 6: # 7th field is first network name (after "AJScan: Filtered networks -")
                    filterednetworkscount += 1
                    date = txts[0]
                    time = txts[1]
                    networks = txts[6:-1] # skip last item "..."
                    #print("$$$ Filtered Networks found = " + ' '.join(networks) + ", line = " + str(linecount))
                    for net in networks: # each network gets own entry
                        filterednetworks.append((date, time, net, linecount))    
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Filtered Networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
                
        if 'Scanning 2Ghz Channels found:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                # Can be empty ...
                if len(txts) > 7: # there is something after the "Scanning 2Ghz Channels found:"
                    channelsfoundcount += 1
                    date = txts[0]
                    time = txts[1]
                    networks = ' '.join(txts[7:])
                    networks2 = networks.split(', ') # parse comma seperated string list
                    #print("@@@ Scanning Channels found: " + ' '.join(networks2) + ", line = " + str(linecount))
                    for net in networks2: # each network gets own entry
                        channelsfound.append((date, time, net, linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Scanning Channels = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                # Can be empty ...
                if len(txts) > 6: # there is something after the "Scanning 2Ghz Channels found:"
                    channelsfoundcount += 1
                    date = txts[0]
                    time = txts[1]
                    networks = ' '.join(txts[6:])
                    networks2 = networks.split(', ') # parse comma seperated string list
                    #print("@@@ Scanning Channels found: " + ' '.join(networks2) + ", line = " + str(linecount))
                    for net in networks2: # each network gets own entry
                        channelsfound.append((date, time, net, linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Scanning Channels = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
                
        if 'Preparing background scan request for ' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 7: # 7th field should contain network name
                    backgroundscancount += 1
                    date = txts[0]
                    time = txts[1]
                    
                    result = re.search('Preparing background scan request for (.*) on channels:', line)
                    #print(result)
                    if (result is None): # search for 2nd variant
                        result = re.search('Preparing background scan request for (.*) Background Scan Caching is Enabled', line)
                    if (result is not None):            
                        networks = result.group(1) # group all network names together via regex
                        networks2 = shlex.split(networks) # split which is "" friendly. It won't break up quoted phrases that have spaces            
                    
                        #print("!!! Background Scan networks found " + ' '.join(networks2) + ", line = " + str(linecount))
                        for net in networks2: # each network gets own entry
                            backgroundscan.append((date, time, net, linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - background scan request = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 6: # 7th field should contain network name
                    backgroundscancount += 1
                    date = txts[0]
                    time = txts[1]
                    
                    result = re.search('Preparing background scan request for (.*) on channels:', line)
                    #print(result)
                    if (result is None): # search for 2nd variant
                        result = re.search('Preparing background scan request for (.*) Background Scan Caching is Enabled', line)
                    if (result is not None):            
                        networks = result.group(1) # group all network names together via regex
                        networks2 = shlex.split(networks) # split which is "" friendly. It won't break up quoted phrases that have spaces            
                    
                        #print("!!! Background Scan networks found " + ' '.join(networks2) + ", line = " + str(linecount))
                        for net in networks2: # each network gets own entry
                            backgroundscan.append((date, time, net, linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - background scan request = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            
        if 'Scanning for MRU Networks:' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 7: # 7th field should contain network name
                    MRUnetworkscount += 1
                    date = txts[0]
                    time = txts[1]
                    # time can be  3/18/2019  6:40:17.341 Scanning for MRU Networks:
                    # or           1/07/2019 19:12:36.354 Scanning for MRU Networks:
                    tlength = len(time) # should be 11 or 12
                    mru = line.split('  ')# double spaces between networks eg "BLAH" on channels: 1  "BLAH2" on channels: 2
                    #print(mru)
                    #print("mru len = " + str(len(mru)))

                    if (tlength == 11):
                    # mru = [' 1/19/2019', '8:46:40.818 Scanning for MRU Networks:', '"Marriott_GUEST" on channels: 136 48 \n']
                        if len(mru) > 2: # has to be something after "Scanning for MRU Networks:" 
                            #print("### MRU networks found: " + ', '.join(mru[2:]) + ", line = " + str(linecount))
                            for m in mru[2:]:
                                MRUnetworks.append((date, time, m.rstrip(), linecount))
                                 
                    if (tlength == 12):
                    # mru = [' 1/07/2019 19:11:57.026 Scanning for MRU Networks:', '"AndroidAP" on channels: 1', '"Vodafone" on channels: 36', '"*WIFI-AIRPORT" on channels: 60 40 \n']
                        if len(mru) > 1: # has to be something after "Scanning for MRU Networks:" 
                            #print("### MRU networks found: " + ', '.join(mru[1:]) + ", line = " + str(linecount))
                            for m in mru[1:]:
                                MRUnetworks.append((date, time, m.rstrip(), linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - MRU networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 6: # 7th field should contain network name
                    MRUnetworkscount += 1
                    date = txts[0]
                    time = txts[1]
                    # time can be  3/18/2019  6:40:17.341 Scanning for MRU Networks:
                    # or           1/07/2019 19:12:36.354 Scanning for MRU Networks:
                    tlength = len(time) # should be 11 or 12
                    mru = line.split('  ')# double spaces between networks eg "BLAH" on channels: 1  "BLAH2" on channels: 2
                    #print(mru)
                    #print("mru len = " + str(len(mru)))

                    if (tlength == 11):
                    # mru = [' 1/19/2019', '8:46:40.818 Scanning for MRU Networks:', '"Marriott_GUEST" on channels: 136 48 \n']
                        if len(mru) > 2: # has to be something after "Scanning for MRU Networks:" 
                            #print("### MRU networks found: " + ', '.join(mru[2:]) + ", line = " + str(linecount))
                            for m in mru[2:]:
                                MRUnetworks.append((date, time, m.rstrip(), linecount))
                                 
                    if (tlength == 12):
                    # mru = [' 1/07/2019 19:11:57.026 Scanning for MRU Networks:', '"AndroidAP" on channels: 1', '"Vodafone" on channels: 36', '"*WIFI-AIRPORT" on channels: 60 40 \n']
                        if len(mru) > 1: # has to be something after "Scanning for MRU Networks:" 
                            #print("### MRU networks found: " + ', '.join(mru[1:]) + ", line = " + str(linecount))
                            for m in mru[1:]:
                                MRUnetworks.append((date, time, m.rstrip(), linecount)) 
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - MRU networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
                
        if '__WiFiDeviceManagerReleasePpmResource: PPM attached - still connected to ' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 10:
                    ppmattachedcount += 1
                    date = txts[0]
                    time = txts[1]
                    net = txts[10:] # Assuming only one entry
                    #print("$$$ PPM attached networks found = " + ' '.join(net).rstrip('.') + ", line = " + str(linecount))
                    ppmattached.append((date, time, ' '.join(net).rstrip('.'), linecount)) # net has . at end
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - PPM attached networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 9:
                    ppmattachedcount += 1
                    date = txts[0]
                    time = txts[1]
                    net = txts[9:] # Assuming only one entry
                    #print("$$$ PPM attached networks found = " + ' '.join(net).rstrip('.') + ", line = " + str(linecount))
                    ppmattached.append((date, time, ' '.join(net).rstrip('.'), linecount)) # net has . at end
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - PPM attached networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1

        if '__WiFiDeviceManagerAutoAssociate: Already connected to ' in line:
             #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 7:
                    alreadyattachedcount += 1
                    date = txts[0]
                    time = txts[1]
                    net = txts[7:] # Assuming only one entry
                    #print("$$$ Already attached networks found = " + ' '.join(net).rstrip('.') + ", line = " + str(linecount))
                    alreadyattached.append((date, time, ' '.join(net).rstrip('.'), linecount)) # net has . at end
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Already attached networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1       

            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 6:
                    alreadyattachedcount += 1
                    date = txts[0]
                    time = txts[1]
                    net = txts[6:] # Assuming only one entry
                    #print("$$$ Already attached networks found = " + ' '.join(net).rstrip('.') + ", line = " + str(linecount))
                    alreadyattached.append((date, time, ' '.join(net).rstrip('.'), linecount)) # net has . at end
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - Already attached networks = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1       

print("\n\n=====================================================")
            
print("\nFound " + str(filterednetworkscount) + " filtered network messages in " + options.inputfile)
print("\nFound " + str(channelsfoundcount) + " found channel messages in " + options.inputfile)
print("\nFound " + str(backgroundscancount) + " background scan channel messages in " + options.inputfile)
print("\nFound " + str(MRUnetworkscount) + " MRU network messages in " + options.inputfile)
print("\nFound " + str(ppmattachedcount) + " PPM attached still connected messages in " + options.inputfile)
print("\nFound " + str(alreadyattachedcount) + " already attached still connected messages in " + options.inputfile)
print("\n=====================================================\n")

if filterednetworkscount > 0:
    f_filtered = open("wifi-buf-net_filtered.TSV", "w")
    f_filtered.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, net, linecount in filterednetworks:
        f_filtered.write(date + "\t" + time + "\tFilteredNetworks\t" + net +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    f_filtered.close()
    print("Logged "+ str(len(filterednetworks)) + " FilteredNetworks to wifi-buf-net_filtered.TSV output file\n")

if channelsfoundcount > 0:
    f_channel = open("wifi-buf-net_channels.TSV", "w")
    f_channel.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, net, linecount in channelsfound:
        f_channel.write(date + "\t" + time + "\tFoundChannels\t" + net +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    f_channel.close()
    print("Logged "+ str(len(channelsfound)) + " FoundChannels to wifi-buf-net_channels.TSV output file\n")

if backgroundscancount > 0:
    f_bgscan = open("wifi-buf-net_bgscan.TSV", "w")
    f_bgscan.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, net, linecount in backgroundscan:
        f_bgscan.write(date + "\t" + time + "\tBGScans\t" + net +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    f_bgscan.close()
    print("Logged "+ str(len(backgroundscan)) + " BGScans to wifi-buf-net_bgscan.TSV output file\n")

if MRUnetworkscount > 0:
    f_mru = open("wifi-buf-net_mru.TSV", "w")
    f_mru.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, m, linecount in MRUnetworks:
        f_mru.write(date + "\t" + time + "\tMRUs\t" + m +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    
    f_mru.close()
    print("Logged "+ str(len(MRUnetworks)) + " MRUs to wifi-buf-net_mru.TSV output file\n")

if ppmattachedcount > 0:
    f_mru = open("wifi-buf-net_ppmattached.TSV", "w")
    f_mru.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, m, linecount in ppmattached:
        f_mru.write(date + "\t" + time + "\tPPMAttached\t" + m +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    
    f_mru.close()
    print("Logged "+ str(len(ppmattached)) + " PPMAttached to wifi-buf-net_ppmattached.TSV output file\n")

if alreadyattachedcount > 0:
    f_mru = open("wifi-buf-net_alreadyattached.TSV", "w")
    f_mru.write("DATE\tTIME\tTYPE\tNETWORK\tLINE\tLOGFILE\n")

    for date, time, m, linecount in alreadyattached:
        f_mru.write(date + "\t" + time + "\tAlreadyAttached\t" + m +"\t" + str(linecount) + "\t" + options.inputfile + "\n")
    
    f_mru.close()
    print("Logged "+ str(len(alreadyattached)) + " AlreadyAttached to wifi-buf-net_alreadyattached.TSV output file\n")
    
print("=====================================================\n") 
print("Ignored " + str(ignorecount) + " malformed entries")   
print("Exiting ...\n")    
    
    

