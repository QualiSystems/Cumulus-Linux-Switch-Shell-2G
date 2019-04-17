from cloudshell.cli.command_template.command_template import CommandTemplate

from package.cloudshell.cumulus.linux.command_templates import ERROR_MAP


SHUTDOWN = CommandTemplate("shutdown -h now", error_map=ERROR_MAP)
