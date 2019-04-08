from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.cli.session.session_exceptions import CommandExecutionException

from package.cloudshell.networking.cumulus.command_templates import enable_disable_snmp


COMMIT_COMMAND_TIMEOUT = 5 * 60


class SnmpV2Actions(object):
    DEFAULT_VIEW_NAME = "Quali"

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
            self._logger.exception("Failed to Enable SNMP on the device:")
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
                                              error_map=error_map).execute_command(snmp_community=snmp_community,
                                                                                   view_name=view_name)
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
            self._logger.exception("Failed to Disable SNMP on the device:")
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=enable_disable_snmp.ABORT,
                                    action_map=action_map,
                                    timeout=COMMIT_COMMAND_TIMEOUT,
                                    error_map=error_map).execute_command()


# class SnmpV3Actions(object):
#     def __init__(self, cli_service, logger, command_modes, user, auth_type, priv_type, password,
#                  priv_key):
#
#         super(SnmpV3Actions, self).__init__(cli_service, logger, command_modes)
#
#         self.user = user
#         self.auth_type = self.get_auth_type(auth_type)
#         self.priv_type = self.get_priv_type(priv_type)
#         self.password = password
#         self.priv_key = priv_key
#
#     @staticmethod
#     def get_auth_type(auth_type):
#         return {
#             'MD5': 'md5',
#             'SHA': 'sha',
#         }.get(auth_type, False)
#
#     @staticmethod
#     def get_priv_type(priv_type):
#         return {
#             'No Privacy Protocol': False,
#             'DES': 'des',
#             'AES-128': 'aes',
#             'AES-256': 'aes256'
#         }[priv_type]
#
#     @property
#     def security_level(self):
#         return {
#             (True, False): 'auth-no-priv',
#             (True, True): 'auth-priv',
#         }.get((bool(self.auth_type), bool(self.priv_type)), False)
#
#     def get_config(self):
#         return self.execute_command(snmp_templates.SHOW_V3_CONF)
#
#     def is_enabled(self):
#         conf = self.get_config()
#
#         return re.search(r'edit "{}"'.format(self.user), conf) is not None
#
#     def enable_snmp(self):
#         edit_snmp_user_mode = EditSnmpUserCommandMode(self.user)
#
#         with self.enter_command_mode(edit_snmp_user_mode):
#             self.execute_command(snmp_templates.SET_STATUS_ENABLE)
#
#             if self.security_level:
#                 self.execute_command(
#                     snmp_templates.SET_SECURITY_LEVEL, security_level=self.security_level)
#                 self.execute_command(snmp_templates.SET_AUTH_PROTO, auth_type=self.auth_type)
#                 self.execute_command(snmp_templates.SET_AUTH_PWD, password=self.password)
#
#                 if self.security_level == 'auth-priv':
#                     self.execute_command(snmp_templates.SET_PRIV_PROTO, priv_type=self.priv_type)
#                     self.execute_command(snmp_templates.SET_PRIV_PWD, priv_key=self.priv_key)
#
#     def disable_snmp(self):
#         with self.enter_command_mode(ConfigSnmpV3CommandMode):
#             self.execute_command(snmp_templates.DELETE_SNMP_USER, user=self.user)
