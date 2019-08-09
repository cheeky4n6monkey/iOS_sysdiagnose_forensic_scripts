#! /usr/bin/env python

# For Python3
# Script to print connection info from logs/appinstallation/AppUpdates.sqlite.db
# Author: david@autopsit.org

import sys
from optparse import OptionParser
import time
import datetime
import sqlite3

version_string = "sysdiagnose-appinstallation.py v2019-08-09 Version 1.0"

if sys.version_info[0] < 3:
    print("Must be using Python 3! Exiting ...")
    exit(-1)

print("Running " + version_string + "\n")

usage = "\n%prog -i inputfile\n"

parser = OptionParser(usage=usage)
parser.add_option("-i", dest="inputfile", 
                  action="store", type="string",
                  help="logs/appinstallation/AppUpdates.sqlite.db to be parsed")
(options, args) = parser.parse_args()

#no arguments given by user, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

try:
    appinstalldb = sqlite3.connect(options.inputfile)
    cursor = appinstalldb.cursor()
    for row in cursor.execute("SELECT pid, bundle_id, install_date FROM app_updates"):
        [pid, bundle_id, install_date] = row

        # convert install_date from Cocoa EPOCH -> UTC
        epoch = install_date + 978307200 # difference between COCOA and UNIX epoch is 978307200 seconds
        utctime = datetime.datetime.utcfromtimestamp(epoch)
        print("%s,%s,%s" % (pid, bundle_id, utctime))
except:
    print("AN UNHANDLED ERRORS OCCURS AND THE DB WAS NOT PARSED")



# That's all folk ;)