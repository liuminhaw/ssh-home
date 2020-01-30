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
        self.CUSTOM= 'CUSTOM'

        # Keys
        self.SHEET_ID = 'sheet-id'
        self.CREDENTIAL_FILE = 'credential-file'
        self.TEMPLATE_SHEET = 'template-sheet'

        # Get config information
        self.candidates = candidates
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(self.candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            raise ConfigNotFoundError(configError)


    def sheet_id(self):
        """
        Return config sheet-id option in CUSTOM section
        If sheet-id not exist, return default value in DEFAULT section
        """
        return self._read_value(self.CUSTOM, self.SHEET_ID)

    def credential_file(self):
        """
        Return config credential-file option in CUSTOM section
        If credential-file not exist, return default value in DEFAULT section
        """
        return self._read_value(self.CUSTOM, self.CREDENTIAL_FILE)

    def template_sheet(self):
        """
        Return config template-sheet option in CUSTOM section
        If template-sheet not exist, return default value in DEFAULT section
        """
        return self._read_value(self.CUSTOM, self.TEMPLATE_SHEET)

    
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