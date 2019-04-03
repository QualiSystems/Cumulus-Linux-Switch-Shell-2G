from cloudshell.devices.snmp_handler import SnmpHandler

from package.cloudshell.networking.cumulus.flows.disable_snmp import CumulusLinuxDisableSnmpFlow
from package.cloudshell.networking.cumulus.flows.enable_snmp import CumulusLinuxEnableSnmpFlow


class CumulusLinuxSnmpHandler(SnmpHandler):
    def __init__(self, resource_config, logger, api, cli_handler):
        super(CumulusLinuxSnmpHandler, self).__init__(resource_config, logger, api)
        self.cli_handler = cli_handler

    def _create_enable_flow(self):
        return CumulusLinuxEnableSnmpFlow(self.cli_handler, self._logger)

    def _create_disable_flow(self):
        return CumulusLinuxDisableSnmpFlow(self.cli_handler, self._logger)
