from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from package.cloudshell.cumulus.linux.command_templates import add_remove_vlan


class VLANActions(object):
    def __init__(self, cli_service, logger):
        """

        :param cli_service:
        :param logger:
        """
        self._cli_service = cli_service
        self._logger = logger

        pass
