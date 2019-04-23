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

    def create_tmp_file(self, action_map=None, error_map=None):
        """

        :param action_map:
        :param error_map:
        :return:
        """
        tmp_file = CommandTemplateExecutor(cli_service=self._cli_service,
                                           command_template=filesystem.CREATE_TEMP_FILE,
                                           action_map=action_map,
                                           remove_prompt=True,
                                           error_map=error_map).execute_command()

        from cloudshell.cli.command_template.command_template import CommandTemplate

        from package.cloudshell.cumulus.linux.command_templates import ERROR_MAP

        CommandTemplate("chmod 755 {}".format(tmp_file.rstrip()), error_map=ERROR_MAP)

        return tmp_file.rstrip()

    def chown_file(self, user_name, file_name, action_map=None, error_map=None):
        """

        :param user_name:
        :param file_name:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=filesystem.CHOWN_FILE,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(user_name=user_name, file_name=file_name)
