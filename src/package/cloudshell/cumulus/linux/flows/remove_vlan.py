from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.devices.flows.cli_action_flows import RemoveVlanFlow


class CumulusLinuxRemoveVlanFlow(RemoveVlanFlow):
    def execute_flow(self, vlan_range, port_name, port_mode, action_map=None, error_map=None):
        pass
