from cloudshell.devices.runners.firmware_runner import FirmwareRunner

from package.cloudshell.cumulus.linux.flows.load_firmware import CumulusLinuxLoadFirmwareFlow


class CumulusLinuxFirmwareRunner(FirmwareRunner):
    @property
    def load_firmware_flow(self):
        return CumulusLinuxLoadFirmwareFlow(cli_handler=self.cli_handler, logger=self._logger)
