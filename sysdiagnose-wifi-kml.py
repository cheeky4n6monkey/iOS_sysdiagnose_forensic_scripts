#! /usr/bin/env python

# For Python3
# Script to print the geolocation values from WiFi/wifi*.log
# and log locations to output KML
# Author: cheeky4n6monkey@gmail.com

#import os
import sys
from optparse import OptionParser
import tarfile

version_string = "sysdiagnose-wifi-kml.py v2019-05-10 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="WiFi/wifi*.log To Be Searched")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

linecount = 0
ignorecount = 0
updatecount = 0
geotagcount = 0
callbackcount = 0
localecallbackcount = 0
checklocalecount = 0
networktranscount = 0
wifimanagercount = 0
wificurrentlocation = 0

locations = []
scanlocations = []
geolocations = []
callbacklocations = []
localecallbacklocations = []
checklocalelocations = []
networktranslocations = []
copylocations = []

#print(options.inputfile[0:-4]) # = wifi-buf-04-26-2019__16:00:52.768.log

if options.inputfile.endswith('.tgz'): # eg wifi-buf-04-26-2019__16:00:52.768.log.tgz
    # untar file first to current directory
    # tarfile.open currently Throws InvalidHeader error!
    with tarfile.open(options.inputfile, 'r:gz') as t:
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
    '''
    for line in data:
        if 'didUpdateLocations:' in line:
            count += 1
            print(line)
    '''       
else: # ass-ume input file has been untarred already and is plaintext
    with open(options.inputfile, 'r') as fp:
         data = fp.readlines()

    for line in data:
        linecount += 1
        
        if 'didUpdateLocations: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    updatecount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("didUpdateLocations dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    locations.append(("didUpdateLocations", linecount, updatecount, date, time, llat, llg, acc, tinterval, src))    
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - didUpdateLocations = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    updatecount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("didUpdateLocations dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    locations.append(("didUpdateLocations", linecount, updatecount, date, time, llat, llg, acc, tinterval, src))    
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - didUpdateLocations = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
        
        elif '__WiFiManagerGeoTagNetwork: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    geotagcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("__WiFiManagerGeoTagNetwork dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    geolocations.append(("__WiFiManagerGeoTagNetwork", linecount, geotagcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiManagerGeoTagNetwork = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    geotagcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("__WiFiManagerGeoTagNetwork dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    geolocations.append(("__WiFiManagerGeoTagNetwork", linecount, geotagcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiManagerGeoTagNetwork = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
                         
        elif '__WiFiManagerLocationManagerCallback: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    callbackcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("__WiFiManagerLocationManagerCallback dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    callbacklocations.append(("__WiFiManagerLocationManagerCallback", linecount, callbackcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiManagerLocationManagerCallback = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1    
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    callbackcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("__WiFiManagerLocationManagerCallback dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    callbacklocations.append(("__WiFiManagerLocationManagerCallback", linecount, callbackcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiManagerLocationManagerCallback = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1    

        elif '__WiFiLocaleManagerLocationManagerCallback: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                # Note: current logs may not contain an location for this
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    localecallbackcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("__WiFiLocaleManagerLocationManagerCallback dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    localecallbacklocations.append(("__WiFiLocaleManagerLocationManagerCallback", linecount, localecallbackcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiLocaleManagerLocationManagerCallback = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    localecallbackcount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("__WiFiLocaleManagerLocationManagerCallback dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    localecallbacklocations.append(("__WiFiLocaleManagerLocationManagerCallback", linecount, localecallbackcount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiLocaleManagerLocationManagerCallback = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
                
        elif 'WiFiLocaleManagerCheckLocale: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                # Note: current logs may not contain an entry for this
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    checklocalecount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("WiFiLocaleManagerCheckLocale dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    checklocalelocations.append(("WiFiLocaleManagerCheckLocale", linecount, checklocalecount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - WiFiLocaleManagerCheckLocale = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    checklocalecount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("WiFiLocaleManagerCheckLocale dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    checklocalelocations.append(("WiFiLocaleManagerCheckLocale", linecount, checklocalecount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - WiFiLocaleManagerCheckLocale = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
         
        elif '__WiFiDeviceManagerAttemptNetworkTransition: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, linecount)
            #print(len(txts))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                # Note: current logs may not contain an entry for this
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    networktranscount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("__WiFiDeviceManagerAttemptNetworkTransition dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    networktranslocations.append(("__WiFiDeviceManagerAttemptNetworkTransition", linecount, networktranscount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiDeviceManagerAttemptNetworkTransition = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    networktranscount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("__WiFiDeviceManagerAttemptNetworkTransition dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + ", line = " + str(linecount))
                    networktranslocations.append(("__WiFiDeviceManagerAttemptNetworkTransition", linecount, networktranscount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiDeviceManagerAttemptNetworkTransition = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
                         
        elif '__WiFiDeviceManagerScanPreviousNetworkChannel: latitude' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                if len(txts) > 8: # latitude is the 4th field but check we have all fields before parsing
                    wifimanagercount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[4][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[5][10:] # strip leading "longitude="
                    acc = txts[6][9:] # strip leading "Accuracy="
                    tinterval = txts[7][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[8][7:] # strip leading "source="
                    #print("__WiFiDeviceManagerScanPreviousNetworkChannel dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + " line = " + str(linecount))
                    scanlocations.append(("__WiFiDeviceManagerScanPreviousNetworkChannel", linecount, wifimanagercount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiDeviceManagerScanPreviousNetworkChannel = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 7: # latitude is the 4th field but check we have all fields before parsing
                    wifimanagercount += 1
                    date = txts[0]
                    time = txts[1]
                    llat = txts[3][9:-1] # strip trailing "," and leading "latitude="
                    llg = txts[4][10:] # strip leading "longitude="
                    acc = txts[5][9:] # strip leading "Accuracy="
                    tinterval = txts[6][21:-4] # strip leading "timeIntervalSinceNow=" and trailing "secs"
                    src = txts[7][7:] # strip leading "source="
                    # print("__WiFiDeviceManagerScanPreviousNetworkChannel dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + " int = " + tinterval + " src = " + src + " line = " + str(linecount))
                    scanlocations.append(("__WiFiDeviceManagerScanPreviousNetworkChannel", linecount, wifimanagercount, date, time, llat, llg, acc, tinterval, src))
                else: 
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - __WiFiDeviceManagerScanPreviousNetworkChannel = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")    
                    ignorecount += 1
                         
        elif 'WiFiManagerCopyCurrentLocation: currentLocation' in line:
            #print("\n" + line)
            txts = line.split()
            #print(txts, str(linecount))
            #print(len(txts))
            if '<NOTICE>:' in line: # current log format has extra <NOTICE>: text after date/time eg "wifi-mm-dd-yyyy__hh[separator]mm[separator]ss.sss.log"
                # Note: current logs may not contain an entry for this
                if len(txts) > 16: # currentLocation pair is the 4th field but check we have all fields before parsing
                    wificurrentlocation += 1
                    date = txts[0]
                    time = txts[1]
                    llat, llg = txts[4][17:-1].split(',') # currentLocation:<+44.38199906,+9.06126224> => +44.38199906,+9.06126224
                    acc = txts[5] + txts[5][:-1] # combine into +/-1433.02
                    speed = txts[8] # speed m/s
                    course = txts[12][:-1] # course
                    atdate = txts[14] # @date
                    attime = txts[15] + " " + txts[16] # @time AM/PM
                    tz = ' '.join(txts[17:]) # ass-ume remainder is timezone. each word is an item in a list so need to join
                    #print(tz)
                    #print("WiFiManagerCopyCurrentLocation dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + \
                    #" spd = " + speed + " course = " + course + " atdate = " + atdate + " attime = " + attime +\
                    #" " + tz + " line = " + str(linecount))
                    # use a separate locations list because of the additional stored values (speed, course etc)
                    copylocations.append(("WiFiManagerCopyCurrentLocation", linecount, wificurrentlocation, date, time, llat, llg, acc, speed, course, atdate, attime, tz, src))
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - WiFiManagerCopyCurrentLocation = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
            else: #archived log format eg WiFiManager/wifi-buf-mm-dd-yyyy__hh-mm-ss.sss.log
                if len(txts) > 15: # currentLocation pair is the 4th field but check we have all fields before parsing
                    wificurrentlocation += 1
                    date = txts[0]
                    time = txts[1]
                    llat, llg = txts[3][17:-1].split(',') # currentLocation:<+44.38199906,+9.06126224> => +44.38199906,+9.06126224
                    acc = txts[4] + txts[5][:-1] # combine into +/-1433.02
                    speed = txts[7] # speed m/s
                    course = txts[11][:-1] # course
                    atdate = txts[13] # @date
                    attime = txts[14] + " " + txts[15] # @time AM/PM
                    tz = ' '.join(txts[16:]) # ass-ume remainder is timezone. each word is an item in a list so need to join
                    #print(tz)
                    # print("WiFiManagerCopyCurrentLocation dt = " + date + " " + time + " llat = " + llat + " llg = " + llg + " acc = " + acc + \
                    # " spd = " + speed + " course = " + course + " atdate = " + atdate + " attime = " + attime +\
                    # " " + tz + " line = " + str(linecount))
                    # use a separate locations list because of the additional stored values (speed, course etc)
                    copylocations.append(("WiFiManagerCopyCurrentLocation", linecount, wificurrentlocation, date, time, llat, llg, acc, speed, course, atdate, attime, tz, src))
                else:
                    #wrong number of fields (eg missing date) ... skip hit completely
                    print("\nERROR - WiFiManagerCopyCurrentLocation = Wrong Number of fields in file (line = " + str(linecount) + ") - Ignoring ...\n")
                    ignorecount += 1
        elif 'latitude' in line: # we get here, something is wrong
            ignorecount += 1
            print("\n\n**** WARNING: Unexpected format for log entry - Ignoring ... ****")
            print(line + " from line = " + str(linecount) + "\n") # malfomed line is ... 

            
print("\n\n=====================================================")            
print("\nFound " + str(updatecount) + " valid didUpdateLocation instances in " + options.inputfile)
print("\nFound " + str(geotagcount) + " valid __WiFiManagerGeoTagNetwork instances in " + options.inputfile)
print("\nFound " + str(callbackcount) + " valid __WiFiManagerLocationManagerCallback instances in " + options.inputfile)
print("\nFound " + str(localecallbackcount) + " valid __WiFiLocaleManagerLocationManagerCallback instances in " + options.inputfile)
print("\nFound " + str(checklocalecount) + " valid WiFiLocaleManagerCheckLocale instances in " + options.inputfile)
print("\nFound " + str(networktranscount) + " valid __WiFiDeviceManagerAttemptNetworkTransition instances in " + options.inputfile)
print("\nFound " + str(wifimanagercount) + " valid __WiFiDeviceManagerScanPreviousNetworkChannel instances in " + options.inputfile)
print("\nFound " + str(wificurrentlocation) + " valid WiFiManagerCopyCurrentLocation instances in " + options.inputfile)
print("\n=====================================================")

if (len(locations)+len(copylocations)+len(scanlocations)+len(geolocations)+len(callbacklocations)+len(localecallbacklocations)+\
    len(checklocalelocations) + len(networktranslocations) > 0):
    f = open("wifi-buf-locations.kml", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    f.write("<Document>")
    f.write("\n<name>" + options.inputfile + "</name><open>1</open>\n")
    f.write("<Folder><name>didUpdateLocation</name><open>0</open>\n")
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in locations: # yellow dot
        f.write("\n<Placemark>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/ms/micons/yellow-dot.png</href></Icon></IconStyle></Style>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")        
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")
    f.write("</Folder>\n")
    f.write("<Folder><name>__WiFiManagerGeoTagNetwork</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in geolocations: #  blue pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")
    f.write("</Folder>\n")
    f.write("<Folder><name>__WiFiManagerLocationManagerCallback</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in callbacklocations: #  pink pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/pink-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")
    f.write("</Folder>\n")
    f.write("<Folder><name>__WiFiLocaleManagerLocationManagerCallback</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in localecallbacklocations: #  purple pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/purple-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>") 
    f.write("</Folder>\n")
    f.write("<Folder><name>WiFiLocaleManagerCheckLocale</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in checklocalelocations: #  light blue pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ltblu-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>") 
    f.write("</Folder>\n")
    f.write("<Folder><name>__WiFiDeviceManagerAttemptNetworkTransition</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in networktranslocations: #  white pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")
    f.write("</Folder>\n")
    f.write("<Folder><name>__WiFiDeviceManagerScanPreviousNetworkChannel</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, tinterval, src in scanlocations: # green pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png</href></Icon></IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")        
    f.write("</Folder>\n")
    f.write("<Folder><name>WiFiManagerCopyCurrentLocation</name><open>0</open>\n")    
    for name, linecount, groupcount, date, time, llat, llg, acc, speed, course, atdate, attime, tz, src in copylocations: # red tinted white pushpin
        f.write("\n<Placemark>\n")
        f.write("<name>" + name + str(groupcount) + "</name>\n")
        f.write("<Style><IconStyle>\n<Icon><href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href></Icon>\n<colorMode>normal</colorMode><color>ff0000ff</color>\n</IconStyle></Style>\n")
        f.write("<description> " + name + " " + str(groupcount) + "\nlat = " + llat + ", long = " + llg + "\n" + date + " " + time + "\naccuracy = " + acc + \
        "\nspeed = " + speed + "\ncourse = " + course + "\nat " + atdate + " " + attime + " " + tz + "\nsource = " + src + "\n\nfile = " + options.inputfile + "\nline = " + str(linecount) + "</description>\n")
        f.write("<Point><coordinates>" + llg + ", " + llat + "</coordinates></Point>\n")
        f.write("</Placemark>")    
    f.write("</Folder>\n")
    f.write("\n</Document>\n")
    f.write("</kml>\n")
    f.close()

    print("\nLogged "+ str(len(locations) + len(geolocations) + len(callbacklocations) +\
    len(localecallbacklocations) + len(checklocalelocations) + len(networktranslocations) + \
    len(scanlocations)  + len(copylocations)) + " locations to wifi-buf-locations.kml output file\n")
    print("Ignored " + str(ignorecount) + " malformed log entries\n")



