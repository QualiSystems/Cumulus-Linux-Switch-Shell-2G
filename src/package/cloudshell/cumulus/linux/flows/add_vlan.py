from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.devices.flows.cli_action_flows import AddVlanFlow


class CumulusLinuxAddVlanFlow(AddVlanFlow):
    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        # ('1000', u'access', u'Cumulus Linux/Chassis 1/Port 1', False, u''
        if qnq:
            pass
        else:
            if port_mode == "trunk":
                # net show interface all
                "net add bridge bridge ports swp1"
                "net add interface swp4 bridge vids 300-500"
            else:
                "net add bridge bridge ports swp1"
                "net add interface swp1 bridge access 100"
