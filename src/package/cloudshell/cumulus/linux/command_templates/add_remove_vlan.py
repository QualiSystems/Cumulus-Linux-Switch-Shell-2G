from cloudshell.cli.command_template.command_template import CommandTemplate

from package.cloudshell.cumulus.linux.command_templates import ERROR_MAP


ADD_PORT_TO_BRIDGE = CommandTemplate("net add bridge bridge ports {port}", error_map=ERROR_MAP)

ALLOW_TRUNK_VLAN_ON_PORT = CommandTemplate("net add interface {port} bridge vids {vlan_range}", error_map=ERROR_MAP)

ADD_ACCESS_VLAN_TO_PORT = CommandTemplate("net add interface {port} bridge access {vlan}", error_map=ERROR_MAP)

REMOVE_PORT_FROM_BRIDGE = CommandTemplate("net del bridge bridge ports {port}", error_map=ERROR_MAP)

REMOVE_TRUNK_VLAN_ON_PORT = CommandTemplate("net del interface {port} bridge vids", error_map=ERROR_MAP)

REMOVE_ACCESS_VLAN_ON_PORT = CommandTemplate("net del interface {port} bridge access", error_map=ERROR_MAP)

# trunk
# ADD_VXLAN_INTERFACE = CommandTemplate("net add vxlan vni-{vlan_c_tag} vxlan id {vlan_c_tag}", error_map=ERROR_MAP)


"net add vxlan vni-1000 bridge learning off"

"net add vxlan vni-1000 bridge access 100"

"net add bridge bridge ports swp3,vni-1000"

# access

"""
net add loopback lo ip address 10.0.0.12/32 ???

cumulus  2001-01-20 17:20:47.108335  net add vxlan vni-1000 vxlan id 1000
cumulus  2001-01-20 17:21:58.863179  net add vxlan vni-1000 bridge learning off
cumulus  2001-01-20 17:22:52.843697  net add vxlan vni-1000 bridge access 100
cumulus  2001-01-20 17:23:16.016229  net add bridge bridge ports vni-1000
cumulus  2001-01-20 17:32:24.093285  net add vxlan vni-1000 bridge l2protocol-tunnel all
"""

"""
WARNING: Committing these changes will cause problems.
vni-1000: missing vxlan-local-tunnelip
"""
