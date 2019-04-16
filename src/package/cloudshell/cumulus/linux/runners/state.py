from cloudshell.devices.runners.state_runner import StateRunner

from package.cloudshell.cumulus.linux.flows.shutdown import CumulusLinuxShutdownFlow


class CumulusLinuxStateRunner(StateRunner):
    def shutdown(self):
        """Shutdown device"""
        return self.shutdown_flow.execute_flow()

    @property
    def shutdown_flow(self):
        return CumulusLinuxShutdownFlow(cli_handler=self.cli_handler, logger=self._logger)
