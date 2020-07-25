# -*- conding: UTF-8 -*-

# Standard library imports
import configparser
import os
import re

class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        """
        # self.HOME = str(pathlib.Path.home())

        # Sections 
        self.GENERAL= 'GENERAL'

        # Keys
        self.SHEET_ID = 'sheet-id'
        self.CREDENTIAL_FILE = 'credential-file'
        self.TEMPLATE_SHEET = 'template-sheet'
        self.SSH_USER = 'ssh-user'
        self.SSH_PORT = 'ssh-port'
        self.SSH_KEY_PATH = 'ssh-key-path'
        self.RSYNC_USER = 'rsync-user'
        self.RSYNC_DEST = 'rsync-dest'
        self.RSYNC_SOURCE = 'rsync-source'
        self.RSYNC_OPTIONS = 'rsync-options'
        self.RSYNC_PORT = 'rsync-port'
        self.RSYNC_KEY_PATH = 'rsync-key-path'
        self.CONNECTION_IP = 'connection-ip'

        # Get config information
        self.candidates = candidates
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(self.candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            raise ConfigNotFoundError(configError)


    def sheet_id(self):
        """
        Return config sheet-id option in GENERAL section
        If sheet-id not exist, return default value in DEFAULT section
        """
        return self._read_value(self.GENERAL, self.SHEET_ID)

    def credential_file(self):
        """
        Return config credential-file option in GENERAL section
        If credential-file not exist, return default value in DEFAULT section
        """
        return self._read_value(self.GENERAL, self.CREDENTIAL_FILE)

    def template_sheet(self):
        """
        Return config template-sheet option in GENERAL section
        If template-sheet not exist, return default value in DEFAULT section
        """
        return self._read_value(self.GENERAL, self.TEMPLATE_SHEET)

    def ssh_user(self, section_name):
        """
        Return config ssh-user option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.SSH_USER)

    def ssh_port(self, section_name):
        """
        Return config ssh-port option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.SSH_PORT)

    def ssh_key_path(self, section_name):
        """
        Return config ssh-key-path option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.SSH_KEY_PATH)

    def rsync_user(self, section_name):
        """
        Return config rsync-user option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_USER)

    def rsync_dest(self, section_name):
        """
        Return config rsync-dest option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_DEST)

    def rsync_source(self, section_name):
        """
        Return config rsync-source option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_SOURCE)

    def rsync_options(self, section_name):
        """
        Return config rsync-options option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_OPTIONS)

    def rsync_port(self, section_name):
        """
        Return config rsync-port option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_PORT)

    def rsync_key_path(self, section_name):
        """
        Return config rsync-key-path option in specific CONNECTION_NAME section
        """
        return self._read_value(section_name, self.RSYNC_KEY_PATH)

    def connection_ip(self, section_name):
        """
        Return config connection_ip option in specific CONNECTION_NAME section
        Return:
            return valid ip address if set
            return 'automatic' if not set
        """
        _connection_ip = self._read_value(section_name, self.CONNECTION_IP, fallback_val='automatic')

        if _connection_ip != 'automatic':
            _ip_range = '[0-9]|[1-8][0-9]|9[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]'
            _pattern = '({range})\.({range})\.({range})\.({range})'.format(range=_ip_range)
            self._validate(_pattern, self.CONNECTION_IP, _connection_ip)

        return _connection_ip

    
    def _read_value(self, section, key, fallback_val=None):
        """
        Get the value of key inside section
        Input:
            section - config file section
            key - config file option
        Return:
            key value
        Error:
            NoSectionError - Section not found
            NoOptionError - Option not found
        """
        try:
            if fallback_val is None:
                _config_value = self._config.get(section, key)
            else:
                _config_value = self._config.get(section, key, fallback=fallback_val)
        except configparser.NoSectionError:
            raise NoSectionError(section)
        except configparser.NoOptionError:
            raise NoOptionError(key)
        else:
            return _config_value

    def _validate(self, pattern, key, value):
        """
        Test to make sure there is value for all options
        Input:
            pattern: regular expression object
            key: string - config option key
            value: string - config option value
        Error:
            raise OptionFormatError if no match found
        """
        _re_pattern = re.compile(r'{}'.format(pattern))

        if _re_pattern.fullmatch(value) == None:
            raise OptionFormatError(key, value)

    # def _section_existence(self, section_name):
    #     """
    #     Check if section_name exist in config file
    #     Return:
    #         True - section_name exist
    #         False - section_name doesn't exist
    #     """
    #     if section_name in self._config.keys():
    #         return True
    #     else:
    #         return False


# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass

class ConfigNotFoundError(configError):
    """
    Raised if not finding ini file
    """
    pass

class NoSectionError(configError):
    """
    Raised by configparser.NoSectionError
    """
    def __init__(self, section):
        self.message = '{} section not found'.format(section)

class NoOptionError(configError):
    """
    Raised by configparser.NoOptionError
    """
    def __init__(self, option):
        self.message = '{} option not found'.format(option)

class OptionFormatError(configError):
    """
    Raised if option is in wrong format
    """
    def __init__(self, option, value):
        self.message = '{} wrong format: {}'.format(option, value)