import datetime
import tempfile

from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.devices.flows.cli_action_flows import SaveConfigurationFlow
from scp import SCPClient

from package.cloudshell.cumulus.linux.command_actions.filesystem import FileSystemActions


class CumulusLinuxSaveFlow(SaveConfigurationFlow):

    CONF_FOLDERS = ("/etc/network/",
                    "/etc/frr/",
                    "/etc/cumulus/acl/*",
                    "/etc/lldpd.d/",
                    "/etc/ssh/")

    CONF_FILES = ("/etc/resolv.conf",
                  "/etc/cumulus/ports.conf",
                  "/etc/cumulus/switchd.conf",
                  "/etc/passwd",
                  "/etc/shadow",
                  "/etc/group",
                  "/etc/lldpd.conf",
                  "/etc/nsswitch.conf",
                  "/etc/sudoers",
                  "/etc/sudoers.d",
                  "/etc/ntp.conf",
                  "/etc/timezone",
                  "/etc/snmp/snmpd.conf",
                  "/etc/default/isc-dhcp-relay",
                  "/etc/default/isc-dhcp-relay6",
                  "/etc/default/isc-dhcp-server",
                  "/etc/default/isc-dhcp-server6",
                  "/etc/cumulus/ports.conf",
                  "/etc/ptp4l.conf",
                  "/etc/hostname",
                  "/etc/vxsnd.conf",
                  "/etc/hosts",
                  "/etc/dhcp/dhclient-exit-hooks.d/dhcp-sethostname",
                  "/usr/lib/python2.7/dist-packages/cumulus/__chip_config/mlx/datapath.conf",
                  "/etc/cumulus/datapath/traffic.conf",
                  "/etc/hostapd.conf",
                  "/etc/security/limits.conf")

    def execute_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """

        :param folder_path:
        :param configuration_type:
        :param vrf_management_name:
        :return:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.root_mode) as cli_service:
            filesystem_actions = FileSystemActions(cli_service=cli_service, logger=self._logger)

            # todo: replace this with temp directory ?
            backup_dir = "BACKUP_{}".format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            filesystem_actions.create_folder(name=backup_dir)

            for conf_folder in self.CONF_FOLDERS:
                filesystem_actions.copy_folder(src_folder=conf_folder, dst_folder=backup_dir)

            for conf_file in self.CONF_FILES:
                filesystem_actions.copy_file(src_file=conf_file, dst_folder=backup_dir)

            backup_file = filesystem_actions.create_tmp_file()
            filesystem_actions.compress_folder(compress_name=backup_file, folder=backup_dir)
            filesystem_actions.remove_folder(name=backup_dir)

            filesystem_actions.chown_file(user_name=cli_service.session.username, file_name=backup_file)

            if not isinstance(cli_service.session, SSHSession):
                raise Exception("Unable to save configuration without CLI type 'SSH'")

            tmp_file_path = tempfile.mktemp(prefix="cumulus_backup_", suffix=".tar")

            scp = SCPClient(transport=cli_service.session._handler.get_transport())
            scp.get(remote_path=backup_file, local_path=tmp_file_path)

            print "*" * 100, tmp_file_path
            # todo:
            # step 2: upload backup file from CS server to remote host
            # step 3: if "File System" - skip this step
