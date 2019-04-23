from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from package.cloudshell.cumulus.linux.command_templates import filesystem


class FileSystemActions(object):
    def __init__(self, cli_service, logger):
        """

        :param cli_service:
        :param logger:
        """
        self._cli_service = cli_service
        self._logger = logger

    def create_folder(self, name, action_map=None, error_map=None):
        """

        :param name:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.CREATE_FOLDER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(name=name)

    def copy_folder(self, src_folder, dst_folder, action_map=None, error_map=None):
        """

        :param src_folder:
        :param dst_folder:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.COPY_FOLDER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(src_folder=src_folder,
                                                                            dst_folder=dst_folder)

    def copy_file(self, src_file, dst_folder, action_map=None, error_map=None):
        """

        :param src_file:
        :param dst_folder:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.COPY_FILE,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(src_file=src_file, dst_folder=dst_folder)

    def compress_folder(self, compress_name, folder, action_map=None, error_map=None):
        """

        :param compress_name:
        :param folder:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.COMPRESS_FOLDER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(compress_name=compress_name, folder=folder)

    def remove_folder(self, name, action_map=None, error_map=None):
        """

        :param name:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.REMOVE_FOLDER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(name=name)
