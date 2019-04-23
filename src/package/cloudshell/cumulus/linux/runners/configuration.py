from cloudshell.devices.runners.configuration_runner import ConfigurationRunner

from package.cloudshell.cumulus.linux.flows.save import CumulusLinuxSaveFlow
from package.cloudshell.cumulus.linux.flows.restore import CumulusLinuxRestoreFlow


class CumulusLinuxConfigurationRunner(ConfigurationRunner):
    @property
    def save_flow(self):
        """

        :return:
        """
        return CumulusLinuxSaveFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def restore_flow(self):
        """

        :return:
        """
        return CumulusLinuxRestoreFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        """

        :return:
        """
        return "file://"
