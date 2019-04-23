import os
import tempfile
import urllib
import ftplib

from cloudshell.devices.networking_utils import UrlParser
import scp
import paramiko
import pysftp
import requests


# todo: move this module to separate package or networking-devices
class AbstractHandler(object):
    def __init__(self, logger):
        """

        :param logger:
        """
        self._logger = logger

    def download(self, file_url):
        """

        :param file_url:
        :return:
        """
        raise NotImplementedError()

    def upload(self, path):
        """

        :param path:
        :return:
        """
        raise NotImplementedError()


class HTTPHandler(AbstractHandler):
    def download(self, file_url):
        """

        :param file_url:
        :return:
        """
        try:
            resp = requests.head(file_url)
        except requests.exceptions.ConnectionError:
            err_msg = "Unable to download configuration file '{}' via HTTP(S). See logs for the details"\
                .format(file_url)
            self._logger.exception(err_msg)
            raise Exception(err_msg)

        resp.raise_for_status()
        tmp_file, _ = urllib.urlretrieve(file_url)

        return tmp_file

    def upload(self, path):
        """

        :param path:
        :return:
        """
        raise Exception("File upload via HTTP(s) is not supported")


class FTPHandler(AbstractHandler):
    def download(self, file_url):
        """

        :param file_url:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_url)
        address = full_path_dict.get(UrlParser.HOSTNAME)
        username = full_path_dict.get(UrlParser.USERNAME)
        password = full_path_dict.get(UrlParser.PASSWORD)
        port = full_path_dict.get(UrlParser.PORT)
        path = full_path_dict.get(UrlParser.PATH)
        filename = full_path_dict.get(UrlParser.FILENAME)
        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        try:
            ftp = ftplib.FTP()
            ftp.connect(host=address, port=port)
            ftp.login(user=username, passwd=password)
            ftp.cwd(path)
            ftp.retrbinary("RETR " + filename, tmp_file.write)
        except:
            err_msg = "Unable to download configuration file '{}' via FTP. See logs for the details".format(file_path)
            self._logger.exception(err_msg)
            raise Exception(err_msg)

        return tmp_file.name

    def upload(self, path):
        pass


class SFTPHandler(AbstractHandler):
    def download(self, file_url):
        """

        :param file_url:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_url)
        address = full_path_dict.get(UrlParser.HOSTNAME)
        username = full_path_dict.get(UrlParser.USERNAME)
        password = full_path_dict.get(UrlParser.PASSWORD)
        port = full_path_dict.get(UrlParser.PORT) or 22
        path = full_path_dict.get(UrlParser.PATH)
        filename = full_path_dict.get(UrlParser.FILENAME)

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        temp_file_path = tempfile.mktemp()

        path_to_file = os.path.join(path, filename)
        self._logger.info("Trying to get file '{}' using SFTP".format(path_to_file))

        try:
            with pysftp.Connection(host=address,
                                   port=port,
                                   username=username,
                                   password=password,
                                   cnopts=cnopts
                                   ) as sftp:
                sftp.get(remotepath=path_to_file, localpath=temp_file_path)
                sftp.close()
        except:
            err_msg = "Unable to download configuration file '{}' via SFTP. See logs for the details".format(file_path)
            self._logger.exception(err_msg)
            raise Exception(err_msg)

        return temp_file_path


class SCPHandler(AbstractHandler):
    def download(self, file_url):
        """

        :param file_url:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_url)
        address = full_path_dict.get(UrlParser.HOSTNAME)
        username = full_path_dict.get(UrlParser.USERNAME)
        password = full_path_dict.get(UrlParser.PASSWORD)
        port = full_path_dict.get(UrlParser.PORT) or 22
        path = full_path_dict.get(UrlParser.PATH)
        filename = full_path_dict.get(UrlParser.FILENAME)
        path_to_file = os.path.join(path, filename)
        temp_file_path = tempfile.mktemp()

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=address, port=port, username=username, password=password)
            client = scp.SCPClient(client.get_transport())
            client.get(remote_path=path_to_file, local_path=temp_file_path)
        except:
            err_msg = "Unable to download configuration file '{}' via SCP. See logs for the details".format(file_path)
            self._logger.exception(err_msg)
            raise Exception(err_msg)

        return temp_file_path


class RemoteClient(object):
    def __init__(self, logger):
        """

        :param logger:
        """
        self._logger = logger
        self._protocol_handler_map = {
            "http": HTTPHandler,
            "https": HTTPHandler,
            "ftp": FTPHandler,
            "sftp": SFTPHandler,
            "scp": SCPHandler,
        }

    def _get_handler(self, file_path):
        """

        :param file_path:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_path)
        self._logger.info("Parsed file link: {}".format(full_path_dict))

        protocol = full_path_dict.get(UrlParser.SCHEME)
        handler = self._protocol_handler_map.get(protocol)

        if handler is None:
            raise Exception("Unable to process file '{}'. Unsupported protocol type '{}'"
                            .format(file_path, protocol))

    def download_file(self, file_url):
        """

        :param file_url:
        :return: file path to the downloaded file
        :rtype: str
        """
        handler = self._get_handler(file_url)
        return handler.download(file_url)

    def upload_file(self, file_path, remote_path):
        """

        :param file_path:
        :return:
        """
        handler = self._get_handler(file_path)
        return handler.upload(file_path)
