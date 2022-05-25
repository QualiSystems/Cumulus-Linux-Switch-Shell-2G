from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    AutoLoadDetails,
    InitCommandContext,
    ResourceCommandContext,
)
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.orchestration_save_restore import OrchestrationSaveRestore
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.command.basic_flow import RunCommandFlow
from cloudshell.shell.flows.connectivity.parse_request_service import (
    ParseConnectivityRequestService,
)
from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel
from cloudshell.shell.standards.networking.driver_interface import (
    NetworkingResourceDriverInterface,
)
from cloudshell.shell.standards.networking.resource_config import (
    NetworkingResourceConfig,
)
from cloudshell.snmp.snmp_configurator import EnableDisableSnmpConfigurator

from cloudshell.cumulus.linux.cli.handler import CumulusCliConfigurator, get_cli
from cloudshell.cumulus.linux.flows.autoload_flow import AutoloadFlow
from cloudshell.cumulus.linux.flows.configuration_flow import ConfigurationFlow
from cloudshell.cumulus.linux.flows.connectivity_flow import CumulusConnectivityFlow
from cloudshell.cumulus.linux.flows.enable_disable_snmp_flow import (
    EnableDisableFlowWithConfig,
)
from cloudshell.cumulus.linux.flows.load_firmware import LoadFirmwareFlow
from cloudshell.cumulus.linux.flows.shutdown import (
    CumulusLinuxShutdownFlow as StateFlow,
)


class CumulusLinuxSwitchShell2GDriver(
    ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock
):
    SUPPORTED_OS = [r"Cumulus"]
    SHELL_NAME = "Cumulus Linux Switch 2G"

    def __init__(self):
        super().__init__()
        self._cli = None

    def _get_resource_conf(self, context, api) -> NetworkingResourceConfig:
        return NetworkingResourceConfig.from_context(
            self.SHELL_NAME, context, api, self.SUPPORTED_OS
        )

    def initialize(self, context: InitCommandContext) -> str:
        resource_config = self._get_resource_conf(context, None)
        self._cli = get_cli(resource_config)
        return "Finished initializing"

    @GlobalLock.lock
    def get_inventory(self, context: AutoLoadCommandContext) -> AutoLoadDetails:
        """Return device structure with all standard attributes."""
        with LoggingSessionContext(context) as logger:
            logger.info("Autoload command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            resource_model = NetworkingResourceModel(
                resource_config.name,
                resource_config.shell_name,
                resource_config.family_name,
            )
            enable_disable_snmp_flow = EnableDisableFlowWithConfig(
                cli_configurator, resource_config, logger
            )
            snmp_configurator = EnableDisableSnmpConfigurator(
                enable_disable_snmp_flow, resource_config, logger
            )
            flow = AutoloadFlow(logger, snmp_configurator)
            response = flow.discover(self.SUPPORTED_OS, resource_model)
            logger.info("Autoload command completed")
            return response

    def restore(
        self,
        context: ResourceCommandContext,
        path: str,
        configuration_type: str,
        restore_method: str,
        vrf_management_name: str,
    ) -> None:
        """Restores a configuration file.

        :param context: The context object for the command with resource and
            reservation info
        :param path: The path to the configuration file, including the configuration
            file name.
        :param restore_method: Determines whether the restore should append or override
            the current configuration.
        :param configuration_type: Specify whether the file should update the startup
            or running config.
        :param vrf_management_name: Optional. Virtual routing and Forwarding management
            name
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Restore command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = ConfigurationFlow(logger, resource_config, cli_configurator)
            flow.restore(path, configuration_type, restore_method, vrf_management_name)
            logger.info("Restore command completed")

    def save(
        self,
        context: ResourceCommandContext,
        folder_path: str,
        configuration_type: str,
        vrf_management_name: str,
    ) -> str:
        """Creates a configuration file and saves it to the provided destination.

        :param context: The context object for the command with resource and
            reservation info
        :param str configuration_type: Specify whether the file should update the
            startup or running config. Value can be running or startup
        :param str folder_path: The path to the folder in which the configuration file
            will be saved.
        :param str vrf_management_name: Optional. Virtual routing and Forwarding
            management name
        :return The configuration file name.
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Save command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = ConfigurationFlow(logger, resource_config, cli_configurator)
            result = flow.save(folder_path, configuration_type, vrf_management_name)
            logger.info("Save command completed")
            return result

    @GlobalLock.lock
    def load_firmware(
        self, context: ResourceCommandContext, path: str, vrf_management_name: str
    ) -> None:
        """Upload and updates firmware on the resource.

        :param context: The context object for the command with resource and
            reservation info
        :param path: path to tftp server where firmware file is stored
        :param vrf_management_name: Optional. Virtual routing and Forwarding
            management name
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Load firmware command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            flow = LoadFirmwareFlow(logger, cli_configurator)
            result = flow.load_firmware(path, vrf_management_name)
            logger.info(f"Finish Load Firmware: {result}")

    def run_custom_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Executes a custom command on the device."""
        with LoggingSessionContext(context) as logger:
            logger.info("Run Custom command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = RunCommandFlow(logger, cli_configurator)
            result = flow.run_custom_command(custom_command)
            logger.info(f"Run Custom command ended with response: {result}")
            return result

    def run_custom_config_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Executes a custom command on the device in configuration mode."""
        with LoggingSessionContext(context) as logger:
            logger.info("Run Custom Config command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = RunCommandFlow(logger, cli_configurator)
            result = flow.run_custom_config_command(custom_command)
            logger.info(f"Run Custom Config command ended with response: {result}")
            return result

    def shutdown(self, context: ResourceCommandContext):
        """Sends a graceful shutdown to the device."""
        with LoggingSessionContext(context) as logger:
            logger.info("Shutdown command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = StateFlow(logger, resource_config, cli_configurator, api)
            return flow.shutdown()

    def orchestration_save(
        self, context: ResourceCommandContext, mode: str, custom_params: str
    ) -> str:
        """Saves the Shell state and returns a description of the saved artifacts.

        This command is intended for API use only by sandbox orchestration scripts to
        implement a save and restore workflow
        :param context: the context object containing resource and reservation info
        :param mode: Snapshot save mode, can be one of two values 'shallow' (default)
            or 'deep'
        :param custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Orchestration save command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )

            if not mode:
                mode = "shallow"

            flow = ConfigurationFlow(logger, resource_config, cli_configurator)
            result = flow.orchestration_save(mode, custom_params)
            response_json = OrchestrationSaveRestore(
                logger, resource_config.name
            ).prepare_orchestration_save_result(result)
            logger.info("Orchestration save command completed")
            return response_json

    def orchestration_restore(
        self,
        context: ResourceCommandContext,
        saved_artifact_info: str,
        custom_params: str,
    ) -> None:
        """Restores a saved artifact previously saved by this Shell driver.

        :param context: The context object for the command with resource and
            reservation info
        :param saved_artifact_info: A JSON string representing the state to restore
            including saved artifacts and info
        :param custom_params: Set of custom parameters for the restore operation
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Orchestration restore command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = ConfigurationFlow(logger, resource_config, cli_configurator)
            restore_params = OrchestrationSaveRestore(
                logger, resource_config.name
            ).parse_orchestration_save_result(saved_artifact_info)
            flow.restore(**restore_params)
            logger.info("Orchestration restore command completed")

    def health_check(self, context: ResourceCommandContext) -> str:
        """Performs device health check.

        :return: Success or Error message
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Health Check command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            flow = StateFlow(logger, resource_config, cli_configurator, api)
            result = flow.health_check()
            logger.info(f"Health Check command ended with result: {result}")
            return result

    def cleanup(self):
        pass

    def ApplyConnectivityChanges(
        self, context: ResourceCommandContext, request: str
    ) -> str:
        """Create vlan and add or remove it to/from network interface."""
        with LoggingSessionContext(context) as logger:
            logger.info("Apply Connectivity command started")
            api = CloudShellSessionContext(context).get_api()
            resource_config = self._get_resource_conf(context, api)
            cli_configurator = CumulusCliConfigurator(
                self._cli, resource_config, logger
            )
            connectivity_request_service = ParseConnectivityRequestService(
                is_vlan_range_supported=True, is_multi_vlan_supported=True
            )
            flow = CumulusConnectivityFlow(
                connectivity_request_service, logger, resource_config, cli_configurator
            )
            result = flow.apply_connectivity(request)
            logger.info(f"Apply connectivity command finished with response {result}")
            return result
