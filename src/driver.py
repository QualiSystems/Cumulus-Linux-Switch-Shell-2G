from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_logger_with_thread_id, get_cli, get_api, parse_custom_commands
from cloudshell.devices.standards.networking.configuration_attributes_structure import \
    create_networking_resource_from_context
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.devices.runners.state_runner import StateRunner
from cloudshell.devices.runners.run_command_runner import RunCommandRunner

from package.cloudshell.networking.cumulus.cli.handler import CumulusCliHandler
from package.cloudshell.networking.cumulus.runners.autoload import CumulusLinuxAutoloadRunner
from package.cloudshell.networking.cumulus.snmp.handler import CumulusLinuxSnmpHandler

# from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface



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

            logger.info('Autoload started')
            response = autoload_operations.discover()
            logger.info('Autoload completed')

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
        pass

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
        pass

    def load_firmware(self, context, cancellation_context, path, vrf_management_name):
        """Upload and updates firmware on the resource

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str path: path to tftp server where firmware file is stored
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        """
        pass

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
        pass

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

        # See below an example implementation, here we use jsonpickle for serialization,
        # to use this sample, you'll need to add jsonpickle to your requirements.txt file
        # The JSON schema is defined at: https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        # You can find more information and examples examples in the spec document at https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        '''
        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.

        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('REPLACE_WITH_ARTIFACT_TYPE', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        return OrchestrationSaveResult(saved_artifacts_info)
        '''
        pass

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """Restores a saved artifact previously saved by this Shell driver using the orchestration_save function

        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        '''
        # The saved_details JSON will be defined according to the JSON Schema and is the same object returned via the
        # orchestration save function.
        # Example input:
        # {
        #     "saved_artifact": {
        #      "artifact_type": "REPLACE_WITH_ARTIFACT_TYPE",
        #      "identifier": "16_08_09 11_21_35_657000"
        #     },
        #     "resource_name": "some_resource",
        #     "restore_rules": {
        #      "requires_same_resource": true
        #     },
        #     "created_date": "2016-08-09T11:21:35.657000"
        #    }

        # The example code below just parses and prints the saved artifact identifier
        saved_details_object = json.loads(saved_details)
        return saved_details_object[u'saved_artifact'][u'identifier']
        '''
        pass

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

            state_operations = StateRunner(logger=logger,
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

    # def ApplyConnectivityChanges(self, context, request):
    #     """Create vlan and add or remove it to/from network interface
    #
    #     :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
    #     :param str request: request json
    #     :return:
    #     """
    #
    #     logger = get_logger_with_thread_id(context)
    #     api = get_api(context)
    #
    #     resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
    #                                                               supported_os=self.SUPPORTED_OS,
    #                                                               context=context)
    #
    #     cli_handler = CliHandler(self._cli, resource_config, logger, api)
    #     connectivity_operations = ConnectivityRunner(logger=logger, cli_handler=cli_handler)
    #     logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
    #     result = connectivity_operations.apply_connectivity_changes(request=request)
    #     logger.info('Finished applying connectivity changes, response is: {0}'.format(str(result)))
    #     logger.info('Apply Connectivity changes completed')
    #
    #     return result


if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

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
                        ("SNMP Version", "2"),
                        ("Enable SNMP", "True"),
                        ("Disable SNMP", "False"),
                        ("SNMP Read Community", "mynotsosecretpassword"),
                        ("Sessions Concurrency Limit", 1),
                        ("CLI Connection Type", "SSH"),
                        ("Password", password)]:

        context.resource.attributes["{}.{}".format(CumulusLinuxSwitchShell2GDriver.SHELL_NAME, attr)] = value


    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.27"

    dr = CumulusLinuxSwitchShell2GDriver()
    dr.initialize(context)

    for res in  dr.get_inventory(context).resources:
        print res.__dict__

    # out = dr.health_check(context)
    # out = dr.run_custom_command(context=context, cancellation_context=None, custom_command="help")
    # out = dr.run_custom_config_command(context=context, cancellation_context=None, custom_command="helpso")


    """
    -bash: helpso: command not found
    
    cumulus@cumulus:~$ net cimmit
    ERROR: Command not found.
    
    """
    # print(out)
