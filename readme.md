I created this script to pull config for live switches on my current Job. It will ssh or telnet into the device pull the configs and saved it on spreadsheet.

How to use it:

Edit the credential files with your credential. Edit the list.txt with the devices ip.
The way I have it is that each branch of my company have two switches, so I had the brachID(can be any) plus two switches seperated by space.

Branchid_1 switch1 switch2

Branchid_2 switch1 switch2

Branchid_3 switch1 switch2

Make sure there is no empty line at the end of the list.

To run the script do the following:
python config_pull.py 1 -> for telnet
python config_pull.py 1 -> for ssh

Use it on your own risk. This script is use for my own purpose and you might need to modified for your need.

You need to install the following modules:
pexpect 
xlwt

