from cloudshell.cli.command_mode import CommandMode


class DefaultCommandMode(CommandMode):
    PROMPT = r"\$\s*$"
    ENTER_COMMAND = ''
    EXIT_COMMAND = 'exit'

    def __init__(self, resource_config, api):
        """Initialize Default command mode, only for cases when session started not in enable mode

        :param resource_config:
        """
        self.resource_config = resource_config
        self._api = api

        super(DefaultCommandMode, self).__init__(DefaultCommandMode.PROMPT,
                                                 DefaultCommandMode.ENTER_COMMAND,
                                                 DefaultCommandMode.EXIT_COMMAND)


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {}
}
