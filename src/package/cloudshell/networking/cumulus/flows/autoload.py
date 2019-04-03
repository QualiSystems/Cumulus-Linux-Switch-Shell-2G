from cloudshell.devices.flows.snmp_action_flows import AutoloadFlow

from package.cloudshell.networking.cumulus.autoload.snmp import CumulusLinuxSNMPAutoload


class CumulusLinuxSnmpAutoloadFlow(AutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        with self._snmp_handler.get_snmp_service() as snmp_service:
            cisco_snmp_autoload = CumulusLinuxSNMPAutoload(snmp_service,
                                                           shell_name,
                                                           shell_type,
                                                           resource_name,
                                                           self._logger)

            return cisco_snmp_autoload.discover(supported_os)
