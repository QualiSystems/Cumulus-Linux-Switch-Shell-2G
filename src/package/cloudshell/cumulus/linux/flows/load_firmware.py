from cloudshell.devices.flows.cli_action_flows import LoadFirmwareFlow

from package.cloudshell.cumulus.linux.command_actions.system import SystemActions
from package.cloudshell.cumulus.linux.command_actions.firmware import FirmwareActions


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
            firmware_actions = FirmwareActions(cli_service=cli_service, logger=self._logger)

            output = firmware_actions.load_firmware(image_path=path, timeout=timeout)

            try:
                output += system_actions.reboot()
            except Exception:
                self._logger.debug("Reboot session exception:", exc_info=True)

            cli_service.reconnect(timeout)
            return output
