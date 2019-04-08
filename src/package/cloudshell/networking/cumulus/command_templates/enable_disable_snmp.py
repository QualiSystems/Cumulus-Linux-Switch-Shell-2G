from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate


ERROR_MAP = OrderedDict([(r'[Cc]ommand not found', 'Command not found'), (r'[Ee]rror:|ERROR:', 'Command error')])

SHOW_SNMP_STATUS = CommandTemplate("net show snmp-server status", error_map=ERROR_MAP)

ADD_LISTENING_ADDRESS = CommandTemplate('net add snmp-server listening-address all', error_map=ERROR_MAP)

CREATE_VIEW = CommandTemplate('net add snmp-server viewname {view_name} included .1', error_map=ERROR_MAP)

ENABLE_SNMP_READ = CommandTemplate('net add snmp-server readonly-community {snmp_community} access any '
                                   'view {view_name}', error_map=ERROR_MAP)

REMOVE_LISTENING_ADDRESS = CommandTemplate('net del snmp-server listening-address all', error_map=ERROR_MAP)

REMOVE_VIEW = CommandTemplate('net del snmp-server viewname {view_name} included .1', error_map=ERROR_MAP)

DISABLE_SNMP_READ = CommandTemplate('net del snmp-server readonly-community {snmp_community} access any '
                                    'view {view_name}', error_map=ERROR_MAP)

COMMIT = CommandTemplate('net commit', error_map=ERROR_MAP)

ABORT = CommandTemplate('net abort', error_map=ERROR_MAP)


"""ENABLE SNMPv3
net add snmp-server username testusernoauth  auth-none
net add snmp-server username testuserauth    auth-md5  myauthmd5password
net add snmp-server username testuserboth    auth-md5  mynewmd5password   encrypt-aes  myencryptsecret
net add snmp-server username limiteduser1    auth-md5  md5password1       encrypt-aes  myaessecret       oid 1.3.6.1.2.1.1
"""


"""
net add snmp-server username testusernoauth  auth-none view cumulusOnly
net add snmp-server username limiteduser1    auth-md5  md5password1 encrypt-aes  myaessecret
"""