from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate


ERROR_MAP = OrderedDict({"[Ii]nvalid\s*([Ii]nput|[Cc]ommand)|[Cc]ommand rejected":
                             "Failed to initialize snmp. Please check Logs for details."})

SHOW_SNMP_STATUS = CommandTemplate("do show running-config | include snmp-server community", error_map=ERROR_MAP)
"""
cumulus@cumulus:~$ net show snmp-server status

Simple Network Management Protocol (SNMP) Daemon.
---------------------------------  ----------------
Current Status                     active (running)
Reload Status                      enabled
Listening IP Addresses             all
Main snmpd PID                     4202
Version 1 and 2c Community String  Configured
Version 3 Usernames                Not Configured
---------------------------------  ---------------- 

"""

# ENABLE_SNMP = CommandTemplate("snmp-server community {snmp_community} {read_only}", error_map=ERROR_MAP)

"""
cumulus@router1:~$ net add snmp-server listening-address all
Configuration has not changed 

cumulus@router1:~$ net add snmp-server readonly-community mynotsosecretpassword access any

cumulus@router1:~$ net add snmp-server system-name my little router

cumulus@router1:~$ net commit

VRF
net add snmp-server listening-address 10.10.10.10 vrf mgmt


"""

"""
disable SNMP?? (will remove all SNMP settings)
net del snmp-server all
"""


""" ENABLE SNMPv3

net add snmp-server username testusernoauth  auth-none
net add snmp-server username testuserauth    auth-md5  myauthmd5password
net add snmp-server username testuserboth    auth-md5  mynewmd5password   encrypt-aes  myencryptsecret
net add snmp-server username limiteduser1    auth-md5  md5password1       encrypt-aes  myaessecret       oid 1.3.6.1.2.1.1

"""

"""
SNMP VIEW?
"""

# https://docs.cumulusnetworks.com/display/DOCS/Simple+Network+Management+Protocol+%28SNMP%29+Monitoring
