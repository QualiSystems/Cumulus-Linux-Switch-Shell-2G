from cloudshell.cli.command_template.command_template import CommandTemplate

from package.cloudshell.cumulus.linux.command_templates import ERROR_MAP


LOAD_FIRMWARE = CommandTemplate('onie-install -fa -i {image_path}', error_map=ERROR_MAP)
