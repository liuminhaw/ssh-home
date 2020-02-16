# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
import sys, os
import pickle, subprocess
from datetime import datetime

# Third party library imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Local application imports
from general_pkg import ssh_home_lib as sh_lib

from module_pkg import conf_mod
from module_pkg import sheet
from module_pkg import logging_class as logcl


CONFIG_FILE = ['config.ini']
LOG_DIR = os.path.join(os.getcwd(), 'logs')

logger = logcl.PersonalLog('home_connect', LOG_DIR)


def main():

    if len(sys.argv) != 2:
        show_help()
        sys.exit(1)
    else:
        connection_name = sys.argv[1]

    # Read ini config file and value
    try:
        config = conf_mod.Config(CONFIG_FILE) 
    except conf_mod.ConfigNotFoundError as err:
        logging = 'Config file config.ini not found: {}'.format(err)
        logger.info(logging)
        sys.exit(11)

    try:
        spreadsheet_id = config.sheet_id()
        credential_file = config.credential_file()
        ssh_user = config.ssh_user(connection_name)
        ssh_port = config.ssh_port(connection_name)
        ssh_key_path = config.ssh_key_path(connection_name)
    except conf_mod.NoSectionError as err:
        logging = 'config.ini section error: {}'.format(err)
        logger.info(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config.ini option error: {}'.format(err)
        logger.info(logging)
        sys.exit(13)

    credential = sh_lib.google_credential(credential_file)
    ip_spreadsheet = sheet.IpSheet(credential, spreadsheet_id)

    # Set date data
    current_datetime = datetime.now()
    current_year = current_datetime.strftime('%Y')
    current_date = current_datetime.strftime('%m/%d/%Y')
    current_time = current_datetime.strftime('%H:%M:%S')

    # Get target sheet (named by current year)
    worksheet_id = ip_spreadsheet.find_sheet_id(current_year)
    if worksheet_id == -1:
        print('Sheet {} not found in spreadsheet {}'.format(current_year, spreadsheet_id))
        sys.exit(5)

    last_row = ip_spreadsheet.get_last_row('{}!A:A'.format(current_year))
    ip_address = ip_spreadsheet.read_ip('{}!C{}'.format(current_year, last_row))

    print('IP Address: {}'.format(ip_address))

    # SSH Connection
    subprocess.run(['ssh', '-i', ssh_key_path, '-p', ssh_port, 
                    '{}@{}'.format(ssh_user, ip_address)])

    print('Disconnected')



def show_help():
    message = \
    """
    USAGE:
        home_connect.py CONNECT_NAME
    DESCRIPTION:
        CONNECT_NAME should be section set inside configurtaion file - config.ini
    """

    print(message)


if __name__ == '__main__':
    # Run codes
    main()

