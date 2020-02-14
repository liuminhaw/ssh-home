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

    
    def _read_value(self, section, key):
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
            _config_value = self._config.get(section, key)
        except configparser.NoSectionError:
            raise NoSectionError(section)
        except configparser.NoOptionError:
            raise NoOptionError(key)
        else:
            return _config_value

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