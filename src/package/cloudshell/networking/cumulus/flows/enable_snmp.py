from cloudshell.devices.flows.cli_action_flows import EnableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters
from cloudshell.snmp.snmp_parameters import SNMPV2WriteParameters
from cloudshell.snmp.snmp_parameters import SNMPV2ReadParameters

from package.cloudshell.networking.cumulus.command_actions.snmp import SnmpV2Actions


class CumulusLinuxEnableSnmpFlow(EnableSnmpFlow):
    def execute_flow(self, snmp_parameters):
        """

        :param cloudshell.snmp.snmp_parameters.SNMPParameters snmp_parameters:
        :return: commands output
        """
        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as cli_service:
            if isinstance(snmp_parameters, SNMPV3Parameters):
                enable_snmp = self._enable_snmp_v3
            else:
                enable_snmp = self._enable_snmp_v2

            enable_snmp(cli_service=cli_service, snmp_parameters=snmp_parameters)

    def _enable_snmp_v2(self, cli_service, snmp_parameters):
        """

        :param cloudshell.cli.cli_service_impl.CliServiceImpl cli_service:
        :param cloudshell.snmp.snmp_parameters.SNMPParameters snmp_parameters:
        :return: commands output
        """
        snmp_community = snmp_parameters.snmp_community

        # todo: check write community

        if not snmp_community:
            raise Exception("SNMP community can not be empty")

        # if isinstance(snmp_parameters, SNMPV2WriteParameters):
        #     read_only_community = False

        snmp_actions = SnmpV2Actions(cli_service=cli_service, logger=self._logger)

        return snmp_actions.enable_snmp(snmp_community=snmp_community)

    def _enable_snmp_v3(self, cli_service, snmp_parameters):
        """

        :param cloudshell.cli.cli_service_impl.CliServiceImpl cli_service:
        :param cloudshell.snmp.snmp_parameters.SNMPParameters snmp_parameters:
        :return: commands output
        """
        pass
