from cloudshell.devices.flows.cli_action_flows import RestoreConfigurationFlow

from package.cloudshell.cumulus.linux.command_actions.system import SystemActions


class CumulusLinuxRestoreFlow(RestoreConfigurationFlow):

    SERVICES_TO_RESTART = ("mstpd",
                           "frr",
                           "sshd",
                           "lldpd",
                           "switchd")

    def execute_flow(self, path, configuration_type, restore_method, vrf_management_name=None):
        """

        :param path:
        :param configuration_type:
        :param restore_method:
        :param vrf_management_name:
        :return:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.root_mode) as cli_service:
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)
            backup_file = system_actions.create_tmp_file()

            system_actions.curl_download_file(remote_url=path, file_path=backup_file)
            system_actions.tar_uncompress_folder(compressed_file=backup_file, destination="/")

            system_actions.if_reload()

            for service in self.SERVICES_TO_RESTART:
                system_actions.restart_service(name=service)
