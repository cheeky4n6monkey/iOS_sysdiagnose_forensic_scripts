# iOS_sysdiagnose_forensic_scripts

iOS devices have the ability to create numerous logs containing forensically useful information.
These logs may contain volatile information which should be collected ASAP during forensic processing.

Dr Mattia Epifani (Twitter: @mattiaep), Heather Mahalik (Twitter: @HeatherMahalik) and @Cheeky4n6monkey have written a document describing their initial research into these logs. This document is freely available from: https://www.for585.com/sysdiagnose
Big Thankyous to Peter Maaswinkel and Pranav Anand for their additional testing and document review.

It is strongly suggested that interested forensic monkeys first read the document BEFORE attempting to use these scripts.
The document details the various iOS logs available, methods of generating and collecting those logs and how to use these scripts to extract forensically interesting information from them.

These scripts were written for Python3 (tested under Ubuntu 16.04 and macOS X Mojave) using test data from various iOS12 devices. They do not require any third party Python libaries.


