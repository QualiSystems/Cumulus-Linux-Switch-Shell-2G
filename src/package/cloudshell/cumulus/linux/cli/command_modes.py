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


class RootCommandMode(CommandMode):
    PROMPT = r"#\s*$"
    ENTER_COMMAND = 'sudo -i'
    EXIT_COMMAND = "exit"

    def __init__(self, resource_config, api):
        """
        Initialize Config command mode
        :param resource_config:
        """

        self.resource_config = resource_config
        self._api = api

        CommandMode.__init__(self,
                             RootCommandMode.PROMPT,
                             RootCommandMode.ENTER_COMMAND,
                             RootCommandMode.EXIT_COMMAND,
                             enter_action_map=self.enter_action_map())

    def enter_action_map(self):
        return {}
        # return {r"{}.*$".format(RootCommandMode.PROMPT): self._check_config_mode}


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        RootCommandMode: {}
    }
}
