from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.devices.flows.cli_action_flows import AddVlanFlow


class CumulusLinuxAddVlanFlow(AddVlanFlow):
    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        import ipdb;ipdb.set_trace()
