from cloudshell.devices.flows.cli_action_flows import SaveConfigurationFlow

from package.cloudshell.cumulus.linux.command_actions.filesystem import FileSystemActions


class CumulusLinuxRestoreFlow(SaveConfigurationFlow):
    def execute_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """

        :param folder_path:
        :param configuration_type:
        :param vrf_management_name:
        :return:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.root_mode) as cli_service:
            filesystem_actions = FileSystemActions(cli_service=cli_service, logger=self._logger)
            # return state_actions.shutdown()