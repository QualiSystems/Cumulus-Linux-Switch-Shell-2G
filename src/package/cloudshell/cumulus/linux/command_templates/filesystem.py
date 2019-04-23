from cloudshell.cli.command_template.command_template import CommandTemplate

from package.cloudshell.cumulus.linux.command_templates import ERROR_MAP


CREATE_FOLDER = CommandTemplate("mkdir -p {name}/", error_map=ERROR_MAP)

COPY_FOLDER = CommandTemplate("cp --parents -rv {src_folder} {dst_folder}/", error_map=ERROR_MAP)

COPY_FILE = CommandTemplate("cp --parents -fv {src_file} {dst_folder}/", error_map=ERROR_MAP)

COMPRESS_FOLDER = CommandTemplate("tar -cvf {compress_name} {folder}", error_map=ERROR_MAP)

REMOVE_FOLDER = CommandTemplate("rm -r {name}/", error_map=ERROR_MAP)
