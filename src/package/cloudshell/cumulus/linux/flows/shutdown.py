from cloudshell.devices.flows.cli_action_flows import ShutdownFlow


class CumulusLinuxShutdownFlow(ShutdownFlow):
    def execute_flow(self):

        with self._cli_handler.get_cli_service(self._cli_handler.root_mode) as cli_service:
            pass
            # iface_action = self._get_iface_actions(config_session)

        "sudo shutdown -h now"
