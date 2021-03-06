from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.cumulus.linux.cli.handler import CumulusCliHandler
from cloudshell.cumulus.linux.runners.autoload import CumulusLinuxAutoloadRunner
from cloudshell.cumulus.linux.runners.connectivity import CumulusLinuxConnectivityRunner
from cloudshell.cumulus.linux.runners.state import CumulusLinuxStateRunner
from cloudshell.cumulus.linux.runners.configuration import CumulusLinuxConfigurationRunner
from cloudshell.cumulus.linux.runners.firmware import CumulusLinuxFirmwareRunner
from cloudshell.cumulus.linux.snmp.handler import CumulusLinuxSnmpHandler
from cloudshell.devices.driver_helper import get_logger_with_thread_id, get_cli, get_api, parse_custom_commands
from cloudshell.devices.standards.networking.configuration_attributes_structure import \
    create_networking_resource_from_context
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.devices.runners.run_command_runner import RunCommandRunner


class CumulusLinuxSwitchShell2GDriver(ResourceDriverInterface, GlobalLock):
    SUPPORTED_OS = [r"Cumulus"]
    SHELL_NAME = "Cumulus Linux Switch 2G"

    def __init__(self):
        """"""
        super(CumulusLinuxSwitchShell2GDriver, self).__init__()
        self._cli = None

    def initialize(self, context):
        """Initialize the driver session

        :param cloudshell.shell.core.driver_context.InitCommandContext context: the context the command runs on
        """
        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)

        return 'Finished initializing'

    @GlobalLock.lock
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: response
        :rtype: str
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Autoload command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            snmp_handler = CumulusLinuxSnmpHandler(resource_config, logger, api, cli_handler)

            autoload_operations = CumulusLinuxAutoloadRunner(logger=logger,
                                                             resource_config=resource_config,
                                                             snmp_handler=snmp_handler)

            response = autoload_operations.discover()
            logger.info('Autoload command completed')

            return response

    def restore(self, context, cancellation_context, path, configuration_type, restore_method, vrf_management_name):
        """Restores a configuration file

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str path: The path to the configuration file, including the configuration file name.
        :param str restore_method: Determines whether the restore should append or override the current configuration.
        :param str configuration_type: Specify whether the file should update the startup or running config.
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Restore command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            if configuration_type.lower() == "startup":
                raise Exception("Shell doesn't support 'Startup' configuration type")

            if restore_method.lower() == "append":
                raise Exception("Shell doesn't support 'Append' restore method")

            configuration_type = "running"
            restore_method = "override"

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            configuration_operations = CumulusLinuxConfigurationRunner(cli_handler=cli_handler,
                                                                       resource_config=resource_config,
                                                                       api=api,
                                                                       logger=logger)

            configuration_operations.restore(path=path,
                                             restore_method=restore_method,
                                             configuration_type=configuration_type,
                                             vrf_management_name=vrf_management_name)

            logger.info("Restore command completed")

    def save(self, context, cancellation_context, folder_path, configuration_type, vrf_management_name):
        """Creates a configuration file and saves it to the provided destination

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str configuration_type: Specify whether the file should update the startup or running config. Value can one
        :param str folder_path: The path to the folder in which the configuration file will be saved.
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        :return The configuration file name.
        :rtype: str
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Save command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            if configuration_type.lower() == "startup":
                raise Exception("Shell doesn't support 'Startup' configuration type")

            configuration_type = 'running'

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            configuration_operations = CumulusLinuxConfigurationRunner(cli_handler=cli_handler,
                                                                       resource_config=resource_config,
                                                                       api=api,
                                                                       logger=logger)

            response = configuration_operations.save(folder_path=folder_path,
                                                     configuration_type=configuration_type,
                                                     vrf_management_name=vrf_management_name)
            logger.info('Save command completed')

            return response

    @GlobalLock.lock
    def load_firmware(self, context, cancellation_context, path, vrf_management_name):
        """Upload and updates firmware on the resource

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str path: path to tftp server where firmware file is stored
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Load firmware command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            if not vrf_management_name:
                vrf_management_name = resource_config.vrf_management_name

            firmware_operations = CumulusLinuxFirmwareRunner(cli_handler=cli_handler, logger=logger)
            response = firmware_operations.load_firmware(path=path, vrf_management_name=vrf_management_name)

            logger.info('Finish Load Firmware: {}'.format(response))

    def run_custom_command(self, context, cancellation_context, custom_command):
        """Executes a custom command on the device

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str custom_command: The command to run. Note that commands that require a response are not supported.
        :return: the command result text
        :rtype: str
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Run Custom command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            send_command_operations = RunCommandRunner(logger=logger,
                                                       cli_handler=cli_handler)

            response = send_command_operations.run_custom_command(custom_command=parse_custom_commands(custom_command))
            logger.info('Run Custom command ended with response: {}'.format(response))

            return response

    def run_custom_config_command(self, context, cancellation_context, custom_command):
        """Executes a custom command on the device in configuration mode

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str custom_command: The command to run. Note that commands that require a response are not supported.
        :return: the command result text
        :rtype: str
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Run Custom Config command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            send_command_operations = RunCommandRunner(logger=logger,
                                                       cli_handler=cli_handler)

            response = send_command_operations.run_custom_config_command(
                custom_command=parse_custom_commands(custom_command))

            logger.info('Run Custom Config command ended with response: {}'.format(response))

            return response

    def shutdown(self, context, cancellation_context):
        """Sends a graceful shutdown to the device

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Shutdown command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            state_operations = CumulusLinuxStateRunner(logger=logger,
                                                       api=api,
                                                       resource_config=resource_config,cli_handler=cli_handler)

            result = state_operations.shutdown()
            logger.info('Shutdown command ended with result: {}'.format(result))

            return result

    def orchestration_save(self, context, cancellation_context, mode, custom_params):
        """Saves the Shell state and returns a description of the saved artifacts and information

        This command is intended for API use only by sandbox orchestration scripts to implement
        a save and restore workflow
        :param ResourceCommandContext context: the context object containing resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str mode: Snapshot save mode, can be one of two values 'shallow' (default) or 'deep'
        :param str custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        :rtype: OrchestrationSaveResult
        """
        logger = get_logger_with_thread_id(context)
        logger.info("Orchestration save command started")

        with ErrorHandlingContext(logger):
            api = get_api(context)
            if not mode:
                mode = 'shallow'

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            configuration_operations = CumulusLinuxConfigurationRunner(cli_handler=cli_handler,
                                                                       resource_config=resource_config,
                                                                       api=api,
                                                                       logger=logger)

            response = configuration_operations.orchestration_save(mode=mode, custom_params=custom_params)
            logger.info('Orchestration save command completed')

            return response

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """Restores a saved artifact previously saved by this Shell driver using the orchestration_save function

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        logger = get_logger_with_thread_id(context)
        logger.info("Orchestration restore command started")

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            configuration_operations = CumulusLinuxConfigurationRunner(cli_handler=cli_handler,
                                                                       resource_config=resource_config,
                                                                       api=api,
                                                                       logger=logger)

            configuration_operations.orchestration_restore(saved_artifact_info=saved_artifact_info,
                                                           custom_params=custom_params)

            logger.info('Orchestration restore command completed')

    def health_check(self, context):
        """Performs device health check

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: Success or Error message
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        logger.info('Health Check command started')

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            state_operations = CumulusLinuxStateRunner(logger=logger,
                                                       api=api,
                                                       resource_config=resource_config,
                                                       cli_handler=cli_handler)

            result = state_operations.health_check()
            logger.info('Health Check command ended with result: {}'.format(result))

            return result

    def cleanup(self):
        """Destroy the driver session, this function is called everytime a driver instance is destroyed

        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    def ApplyConnectivityChanges(self, context, request):
        """
        Create vlan and add or remove it to/from network interface
        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param str request: request json
        :return:
        """

        logger = get_logger_with_thread_id(context)
        logger.info('Apply connectivity changes command started with request: {}'.format(request))

        with ErrorHandlingContext(logger):
            api = get_api(context)

            resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                      supported_os=self.SUPPORTED_OS,
                                                                      context=context)

            cli_handler = CumulusCliHandler(cli=self._cli,
                                            resource_config=resource_config,
                                            logger=logger,
                                            api=api)

            connectivity_operations = CumulusLinuxConnectivityRunner(cli_handler=cli_handler,
                                                                     logger=logger)

            result = connectivity_operations.apply_connectivity_changes(request=request)
            logger.info('Apply connectivity changes command completed with response: {}'.format(result))

            return result


if __name__ == "__main__":
    import json
    import mock
    from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    def prepare_context():
        """

        :return:
        """
        """Return initialized driver instance"""
        address = '192.168.105.30'
        user = 'cumulus'
        password = 'CumulusLinux!'
        port = 443
        auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
        api_port = 8029

        context = ResourceCommandContext(*(None,) * 4)
        context.resource = ResourceContextDetails(*(None,) * 13)
        context.resource.name = "Cumulus Linux Switch"
        context.resource.fullname = "Cumulus Linux Switch"
        context.resource.address = address
        context.resource.family = "CS_Switch"
        context.reservation = ReservationContextDetails(*(None,) * 7)
        context.reservation.reservation_id = '0cc17f8c-75ba-495f-aeb5-df5f0f9a0e97'
        context.resource.attributes = {}

        for attr, value in [("User", user),
                            ("Sessions Concurrency Limit", 1),

                            # Backup location attributes for the "Save" command
                            ("Backup Location", "/home/cumulus/backups"),
                            ("Backup Type", "File System"),
                            ("Backup User", "backup_user"),
                            ("Backup Password", "backup_pass"),

                            # Backup location attributes for the "Save" command
                            # ("Backup Location", "192.168.85.13/home/quali/"),
                            # ("Backup Type", "scp"),
                            # ("Backup User", "quali"),
                            # ("Backup Password", "quali"),


                            # SNMP v2 Read-only
                            # ("SNMP Version", "2"),
                            # ("Enable SNMP", "True"),
                            # ("Disable SNMP", "True"),
                            # ("SNMP Read Community", "mynotsosecretpassword"),
                            # End SNMP v2 Read-only

                            # SNMP v2 Read-Write
                            # ("SNMP Version", "2"),
                            # ("Enable SNMP", "True"),
                            # ("Disable SNMP", "False"),
                            # ("SNMP Write Community", "public"),
                            # End SNMP v2 Read-Write

                            # SNMP v3
                            ("SNMP Version", "3"),
                            ("Enable SNMP", "True"),
                            ("Disable SNMP", "True"),
                            ("SNMP V3 User", "quali"),
                            ("SNMP V3 Password", "qualipass"),
                            ("SNMP V3 Private Key", "qualipass2"),
                            ("SNMP V3 Authentication Protocol", "No Authentication Protocol"),
                            # "No Authentication Protocol", "MD5", "SHA"
                            ("SNMP V3 Privacy Protocol", "No Privacy Protocol"),
                            # "No Privacy Protocol", "DES", "3DES-EDE", "AES-128", "AES-192", "AES-256"
                            # End SNMP v3

                            ("Sessions Concurrency Limit", 1),
                            ("CLI Connection Type", "SSH"),
                            ("Password", password),
                            ("Enable Password", password)]:

            context.resource.attributes["{}.{}".format(CumulusLinuxSwitchShell2GDriver.SHELL_NAME, attr)] = value
            context.connectivity = mock.MagicMock()
            context.connectivity.server_address = "192.168.85.10"

        return context

    def get_driver(context):
        """

        :return:
        """
        dr = CumulusLinuxSwitchShell2GDriver()
        dr.initialize(context)
        return dr

    def get_inventory(driver, context):
        """

        :param driver:
        :return:
        """
        return [res.__dict__ for res in driver.get_inventory(context).resources]

    def health_check(driver, context):
        """

        :param driver:
        :return:
        """
        return driver.health_check(context)

    def shutdown(driver, context):
        """

        :param driver:
        :return:
        """
        return driver.shutdown(context, None)

    def run_custom_command(driver, context, custom_command="help"):
        """

        :param driver:
        :param context:
        :param custom_command:
        :return:
        """
        return driver.run_custom_command(context=context, cancellation_context=None, custom_command=custom_command)

    def run_custom_config_command(driver, context, custom_command="help"):
        """

        :param driver:
        :param context:
        :param custom_command:
        :return:
        """
        return driver.run_custom_config_command(context=context, cancellation_context=None, custom_command=custom_command)

    def save(driver, context, folder_path, configuration_type, vrf_management_name=""):
        """
        
        :param driver: 
        :param context: 
        :param folder_path: 
        :param configuration_type: 
        :param vrf_management_name: 
        :return: 
        """
        return driver.save(context=context,
                           cancellation_context=None,
                           folder_path=folder_path,
                           configuration_type=configuration_type,
                           vrf_management_name=vrf_management_name)

    def restore(driver, context, path, configuration_type, restore_method, vrf_management_name=""):
        """

        :param driver:
        :param context:
        :param path:
        :param configuration_type:
        :param restore_method:
        :param vrf_management_name:
        :return:
        """
        return driver.restore(context=context,
                              cancellation_context=None,
                              path=path,
                              configuration_type=configuration_type,
                              restore_method=restore_method,
                              vrf_management_name=vrf_management_name)

    def load_firmware(driver, context, path, vrf_management_name=""):
        """

        :param driver:
        :param context:
        :param path:
        :param vrf_management_name:
        :return:
        """
        return driver.load_firmware(context=context,
                                    cancellation_context=None,
                                    path=path,
                                    vrf_management_name=vrf_management_name)

    def apply_connectivity_changes(driver, context, action="setVlan"):
        """

        :param driver:
        :param context:
        :param request:
        :return:
        """
        request = {"driverRequest": {"actions": [{"connectionId": "22ec7879-e996-4f9a-83ab-bf24f1107281",
                                                  "connectionParams": {"vlanId": "1000", "mode": "Access",
                                                                       "vlanServiceAttributes": [
                                                                           {"attributeName": "QnQ",
                                                                            "attributeValue": "False",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "CTag",
                                                                            "attributeValue": "",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "Isolation Level",
                                                                            "attributeValue": "Shared",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "Access Mode",
                                                                            "attributeValue": "Access",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "VLAN ID",
                                                                            "attributeValue": "10",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "Pool Name",
                                                                            "attributeValue": "",
                                                                            "type": "vlanServiceAttribute"},
                                                                           {"attributeName": "Virtual Network",
                                                                            "attributeValue": "255",
                                                                            "type": "vlanServiceAttribute"}],
                                                                       "type": "setVlanParameter"},
                                                  "connectorAttributes": [],
                                                  "actionId": "22ec7879-e996-4f9a-83ab-bf24f1107281_085a8f57-d09d-4f92-9201-0da098d14c06",
                                                  "actionTarget": {
                                                      "fullName": "Cumulus Linux/Chassis 1/Port 1",
                                                      "fullAddress": "192.168.105.30/CH1/P1",
                                                      "type": "actionTarget"},
                                                  "customActionAttributes": [], "type": action}]}}

        return dr.ApplyConnectivityChanges(context, json.dumps(request))

    context = prepare_context()
    dr = get_driver(context)

    # get inventory
    # print get_inventory(driver=dr, context=context)

    # # health check
    # print health_check(driver=dr, context=context)
    #
    # # shutdown
    # print shutdown(driver=dr, context=context)
    #
    # # run custom command
    # print run_custom_command(driver=dr, context=context)
    #
    # # run custom config command
    # print run_custom_config_command(driver=dr, context=context)
    #
    # # run save command
    # print save(driver=dr,
    #            context=context,
    #            folder_path="",
    #            configuration_type="running",
    #            vrf_management_name="")
    #
    # print save(driver=dr,
    #            context=context,
    #            folder_path="scp://quali:quali@192.168.85.13/home/quali",
    #            configuration_type="shalk",
    #            vrf_management_name="")
    #
    # print save(driver=dr,
    #            context=context,
    #            folder_path="ftp://test_user:test_password@192.168.42.102",
    #            configuration_type="shalk",
    #            vrf_management_name="")
    #
    # print restore(driver=dr,
    #               context=context,
    #               path="ftp://test_user:test_password@192.168.42.102/Cumulus_Linux_Switch-running-240419-180106",
    #               configuration_type="running",
    #               restore_method="override",
    #               vrf_management_name="")
    #
    print load_firmware(driver=dr,
                        context=context,
                        path="ftp://test_user:test_password@192.168.42.102/Cumulus_Linux_Switch-running-240419-180106")

    # # run apply connectivity changes | set VLAN
    # print apply_connectivity_changes(driver=dr, context=context, action="setVlan")
    #
    # # run apply connectivity changes | remove VLAN
    # print apply_connectivity_changes(driver=dr, context=context, action="removeVlan")
