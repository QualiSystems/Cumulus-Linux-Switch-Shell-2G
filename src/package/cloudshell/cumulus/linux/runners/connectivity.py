from cloudshell.devices.runners.connectivity_runner import ConnectivityRunner

from package.cloudshell.cumulus.linux.flows.add_vlan import CumulusLinuxAddVlanFlow
from package.cloudshell.cumulus.linux.flows.remove_vlan import CumulusLinuxRemoveVlanFlow


class CumulusLinuxConnectivityRunner(ConnectivityRunner):
    @property
    def add_vlan_flow(self):
        return CumulusLinuxAddVlanFlow(self.cli_handler, self._logger)

    @property
    def remove_vlan_flow(self):
        return CumulusLinuxRemoveVlanFlow(self.cli_handler, self._logger)
