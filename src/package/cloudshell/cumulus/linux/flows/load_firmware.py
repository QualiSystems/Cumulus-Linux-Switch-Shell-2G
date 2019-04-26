from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.devices.flows.cli_action_flows import LoadFirmwareFlow

from package.cloudshell.cumulus.linux.command_actions.commit import CommitActions
from package.cloudshell.cumulus.linux.command_actions.filesystem import SystemActions


class CumulusLinuxLoadFirmwareFlow(LoadFirmwareFlow):
    def execute_flow(self, path, vrf, timeout):
        """

        :param path:
        :param vrf:
        :param timeout:
        :return:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.root_mode) as cli_service:
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)
            commit_actions = CommitActions(cli_service=cli_service, logger=self._logger)

            # todo: backup and copy back directories if something went wrong during the upgrade

            # step 1: backup data
            # step 2: upgrade system
            # sudo onie-install -fa -i http://10.0.1.251/cumulus-linux-3.7.1-mlx-amd64.bin && sudo reboot
            # step 4: reboot
            # step 3: restore backup-ed data
            # error: Failure:

            try:
                pass
            except CommandExecutionException:
                self._logger.exception("Failed to load filmware:")
                commit_actions.abort()
                raise
