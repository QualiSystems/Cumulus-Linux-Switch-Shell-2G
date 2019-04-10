from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from package.cloudshell.cumulus.linux.command_templates import enable_disable_snmp


COMMIT_COMMAND_TIMEOUT = 5 * 60
DEFAULT_VIEW_NAME = "Quali"


class SnmpV2Actions(object):
    def __init__(self, cli_service, logger):
        """

        :param cli_service:
        :param logger:
        """
        self._cli_service = cli_service
        self._logger = logger

    def enable_snmp(self, snmp_community, view_name=DEFAULT_VIEW_NAME, action_map=None, error_map=None):
        """

        :param snmp_community:
        :param view_name:
        :param action_map:
        :param error_map:
        :return:
        """
        try:
            output = CommandTemplateExecutor(cli_service=self._cli_service,
                                             command_template=enable_disable_snmp.ADD_LISTENING_ADDRESS,
                                             action_map=action_map,
                                             error_map=error_map).execute_command()

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.CREATE_VIEW,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(view_name=view_name)

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.ENABLE_SNMP_READ,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(snmp_community=snmp_community,
                                                                                   view_name=view_name)

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.COMMIT,
                                              action_map=action_map,
                                              timeout=COMMIT_COMMAND_TIMEOUT,
                                              error_map=error_map).execute_command()
            return output

        except CommandExecutionException:
            self._logger.exception("Failed to Enable SNMPv2 on the device:")
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ABORT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()

    def disable_snmp(self, snmp_community, view_name=DEFAULT_VIEW_NAME, action_map=None, error_map=None):
        """

        :param snmp_community:
        :param view_name:
        :param action_map:
        :param error_map:
        :return:
        """
        try:
            output = CommandTemplateExecutor(cli_service=self._cli_service,
                                             command_template=enable_disable_snmp.REMOVE_LISTENING_ADDRESS,
                                             action_map=action_map,
                                             error_map=error_map).execute_command()

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.DISABLE_SNMP_READ,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(snmp_community=snmp_community)

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.REMOVE_VIEW,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(view_name=view_name)

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.COMMIT,
                                              action_map=action_map,
                                              timeout=COMMIT_COMMAND_TIMEOUT,
                                              error_map=error_map).execute_command()
            return output

        except CommandExecutionException:
            self._logger.exception("Failed to Disable SNMPv2 on the device:")
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ABORT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()


class SnmpV3Actions(object):

    AUTH_COMMAND_MAP = {
        SNMPV3Parameters.AUTH_NO_AUTH: "auth-none",
        SNMPV3Parameters.AUTH_MD5: "auth-md5",
        SNMPV3Parameters.AUTH_SHA: "auth-sha"
    }

    PRIV_COMMAND_MAP = {
        SNMPV3Parameters.PRIV_NO_PRIV: "",
        SNMPV3Parameters.PRIV_DES: "encrypt-des",
        # SNMPV3Parameters.PRIV_3DES: "",  # not supported by device
        SNMPV3Parameters.PRIV_AES128: "encrypt-aes",  # todo: verify AES that corresponds to the cumulus
        SNMPV3Parameters.PRIV_AES192: "encrypt-aes",  # todo: verify AES that corresponds to the cumulus
        SNMPV3Parameters.PRIV_AES256: "encrypt-aes"  # todo: verify AES that corresponds to the cumulus
    }

    def __init__(self, cli_service, logger):
        """

        :param cli_service:
        :param logger:
        """
        self._cli_service = cli_service
        self._logger = logger

    def enable_snmp(self, snmp_user, snmp_password, snmp_priv_key, snmp_auth_proto, snmp_priv_proto,
                    view_name=DEFAULT_VIEW_NAME, action_map=None, error_map=None):
        """

        :param snmp_user:
        :param snmp_password:
        :param snmp_priv_key:
        :param snmp_auth_proto:
        :param snmp_priv_proto:
        :param view_name:
        :param action_map:
        :param error_map:
        :return:
        """
        try:
            auth_command_template = self.AUTH_COMMAND_MAP[snmp_auth_proto]
        except KeyError:
            raise Exception("Authentication protocol {} is not supported".format(snmp_auth_proto))

        try:
            priv_command_template = self.PRIV_COMMAND_MAP.get(snmp_priv_proto)
        except KeyError:
            raise Exception("Privacy Protocol {} is not supported".format(snmp_priv_proto))

        try:
            output = CommandTemplateExecutor(cli_service=self._cli_service,
                                             command_template=enable_disable_snmp.ADD_LISTENING_ADDRESS,
                                             action_map=action_map,
                                             error_map=error_map).execute_command()

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.CREATE_VIEW,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(view_name=view_name)

            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ENABLE_SNMP_USER,
                                    action_map=action_map,
                                    error_map=error_map).execute_command(snmp_user=snmp_user,
                                                                         snmp_auth_proto=auth_command_template,
                                                                         snmp_password=snmp_password,
                                                                         snmp_priv_proto=priv_command_template,
                                                                         snmp_priv_key=snmp_priv_key,
                                                                         view_name=view_name)

            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.COMMIT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()

        except CommandExecutionException:
            self._logger.exception("Failed to Enable SNMPv3 on the device:")
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ABORT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()

    def disable_snmp(self, snmp_user, view_name=DEFAULT_VIEW_NAME, action_map=None, error_map=None):
        """

        :param snmp_user:
        :param view_name:
        :param action_map:
        :param error_map:
        :return:
        """
        try:
            output = CommandTemplateExecutor(cli_service=self._cli_service,
                                             command_template=enable_disable_snmp.REMOVE_LISTENING_ADDRESS,
                                             action_map=action_map,
                                             error_map=error_map).execute_command()

            output += CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=enable_disable_snmp.REMOVE_VIEW,
                                              action_map=action_map,
                                              error_map=error_map).execute_command(view_name=view_name)

            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.DISABLE_SNMP_USER,
                                    action_map=action_map,
                                    error_map=error_map).execute_command(snmp_user=snmp_user)

            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.COMMIT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()

        except CommandExecutionException:
            self._logger.exception("Failed to Enable SNMPv3 on the device:")
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ABORT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()
