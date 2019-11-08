# iOS_sysdiagnose_forensic_scripts

<br>
<p align="center">
<img src="log-monkey.png" alt="Picture of Apple Log Loving Monkey")
</p>
<br>

iOS devices have the ability to create numerous logs containing forensically useful information.
These logs may contain volatile information which should be collected ASAP during forensic processing.

<b>Mattia Epifani (Github: mattiaepi , [Twitter: @mattiaep](https://twitter.com/mattiaep)) </b>, <b>Heather Mahalik (Github: hmahalik , [Twitter: @HeatherMahalik](https://twitter.com/HeatherMahalik))</b> and <b>[@Cheeky4n6monkey](https://twitter.com/cheeky4n6monkey)</b> have written a document describing their initial research into these logs. This document is freely available from:
<p align="center"><b>https://www.for585.com/sysdiagnose</b></p>

<p>Big Thankyous to <b>Peter Maaswinkel</b> and <b>Pranav Anand</b> for their additional testing and document review.<p>
<p>Thanks also to <b>David Durvaux (ddurvaux)</b> for sharing his script - <b>sysdiagnose-appupdates.py</b><p>
<p>Thanks to <b>Silvia Spallarossa<b> for her testing of the scripts and bug fixes for <b>sysdiagnose-networkinterfaces.py<b>.<p>

It is strongly suggested that interested forensic monkeys first read the document BEFORE attempting to use these scripts.
The document details the various iOS logs available, methods of generating and collecting those logs and how to use these scripts to extract forensically interesting information from them.

These scripts were written for <b>Python3</b> (tested under Ubuntu 16.04 and macOS X Mojave) using test data from various <b>iOS12</b> devices. They do not require any third party Python libaries.
<br>

Here is a usage summary of the available scripts:
<table>
  <tr><td><b>Name</b></td><td><b>Description</b></td><td><b>Output</b></td><td><b>Usage Example</b></td></tr>
  <tr><td>sysdiagnose-sys.py</td><td>Extracts OS info from logs/SystemVersion/SystemVersion.plist</td><td>Command line</td><td>python3 sysdiagnose-sys.py -i SystemVersion.plist</td></tr>
  
  <tr><td>sysdiagnose-networkprefs.py</td><td>Extracts hostnames from logs/Networking/preferences.plist</td><td>Command line</td><td>python3 sysdiagnose-networkprefs.py -i preferences.plist</td></tr>
  
  <tr><td>sysdiagnose-networkinterfaces.py</td><td>Extracts network config info from logs/Networking/NetworkInterfaces.plist</td><td>Command line</td><td>python3 sysdiagnose-networkinterfaces.py -i NetworkInterfaces.plist</td></tr>
  
  <tr><td>sysdiagnose-mobilecontainermanager.py</td><td>Extracts uninstall info from logs/MobileContainerManager/containermanagerd.log.0</td><td>Command line</td><td>python3 sysdiagnose-mobilecontainermanager.py -i containermanagerd.log.0</td></tr>
  
  <tr><td>sysdiagnose-mobilebackup.py</td><td>Extracts backup info from logs/MobileBackup/com.apple.MobileBackup.plist</td><td>Command line</td><td>python3 sysdiagnose-mobilebackup.py -i com.apple.MobileBackup.plist</td></tr>
  
  <tr><td>sysdiagnose-mobileactivation.py</td><td>Mobile Activation Startup and Upgrade info from logs/MobileActivation/mobileactivationd.log.*</td><td>Command line</td><td>python3 sysdiagnose-mobileactivation.py -i mobileactivation.log</td></tr>
  
  <tr><td>sysdiagnose-wifi-plist.py</td><td>Extracts Wi-Fi network values from WiFi/com.apple.wifi.plist<br>Use -t option for TSV output file
</td><td>Command line and TSV</td><td>python3 sysdiagnose-wifi-plist.py -i com.apple.wifi.plist -t</td></tr>
  
  <tr><td>sysdiagnose-wifi-icloud.py</td><td>Extracts Wi-Fi network values from WiFi/ICLOUD.apple.wifid.plist<br>Use -t option for TSV output file</td><td>Command line and TSV</td><td>python3 sysdiagnose-wifi-icloud.py -i ICLOUD.apple.wifid.plist -t</td></tr>
  
  <tr><td>sysdiagnose-wifi-net.py</td><td>Extracts Wi-Fi network names to categorized TSV files from WiFi/wifi *.log</td><td>TSV files</td><td>python3 sysdiagnose-wifi-net.py -i wifi-buf.log</td></tr>
  
  <tr><td>sysdiagnose-wifi-kml.py</td><td>Extracts Wi-Fi geolocation values and creates a KML from wifi*.log</td><td>KML</td><td>python3 sysdiagnose-wifi-kml.py -i wifi-buf.log</td></tr>
  
  <tr><td>sysdiagnose-uuid2path.py</td><td>Extracts GUID and path info from logs/tailspindb/UUIDToBinaryLocations</td><td>Command line (comma separated)</td><td>python3 sysdiagnose-uuid2path.py  -i UUIDToBinaryLocations</td></tr>
  
  <tr><td>sysdiagnose-net-ext-cache.py</td><td>Extracts app name & GUID info from logs/Networking/com.apple.networkextension.cache.plist<br>Use -v option to print GUID info</td><td>Command line</td><td>python3 sysdiagnose-net-ext-cache.py -i com.apple.networkextension.cache.plist -v</td></tr>
  
  <tr><td>sysdiagnose-appconduit.py</td><td>Extracts connection info from logs/AppConduit/AppConduit.log.*</td><td>Command line</td><td>python3 sysdiagnose-appconduit.py -i AppConduit.log</td></tr>
  
  <tr><td>sysdiagnose-appupdates.py</td><td>Extracts update info from logs/appinstallation/AppUpdates.sqlite.db.*</td><td>Command line</td><td>python3 sysdiagnose-appupdates.py -i AppUpdates.sqlitedb</td></tr>
  
</table>
  
