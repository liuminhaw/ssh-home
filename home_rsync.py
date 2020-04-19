# -*- coding:UTF-8 -*-

# Standard library imports
import sys, os
import pickle, subprocess
import argparse
from datetime import datetime

# Third party library imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Local application imports
from general_pkg import env
from general_pkg import credential as cred

from module_pkg import conf_mod
from module_pkg import sheet
from module_pkg import logging_class as logcl


logger = logcl.PersonalLog('home_rsync', env.LOG_DIR)

def main():

    # arguments definition
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('connection', help='Section name set in configuration file - config.ini')
    # arg_parser.add_argument("-V", "--version", help="show program version", action="store_true")
    arg_parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(env.VERSION))
    args = arg_parser.parse_args()

    connection_name = args.connection
    logger.info('Connection name: {}'.format(connection_name))

    # Read ini config file and value
    try:
        config = conf_mod.Config(env.CONFIG_FILE) 
    except conf_mod.ConfigNotFoundError as err:
        logging = 'Config file config.ini not found: {}'.format(err)
        logger.info(logging)
        sys.exit(11)

    try:
        spreadsheet_id = config.sheet_id()
        credential_file = config.credential_file()
        rsync_user = config.rsync_user(connection_name)
        rsync_dest = config.rsync_dest(connection_name)
        rsync_source = config.rsync_source(connection_name)
        rsync_options = config.rsync_options(connection_name)
        rsync_port = config.rsync_port(connection_name)
        rsync_key_path = config.rsync_key_path(connection_name)
    except conf_mod.NoSectionError as err:
        logging = 'config.ini section error: {}'.format(err)
        logger.info(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config.ini option error: {}'.format(err)
        logger.info(logging)
        sys.exit(13)

    credential = cred.google_credential(credential_file)
    ip_spreadsheet = sheet.IpSheet(credential, spreadsheet_id)

    # Set date data
    current_datetime = datetime.now()
    current_year = current_datetime.strftime('%Y')

    # Get target sheet (named by current year)
    worksheet_id = ip_spreadsheet.find_sheet_id(current_year)
    if worksheet_id == -1:
        print('Sheet {} not found in spreadsheet {}'.format(current_year, spreadsheet_id))
        sys.exit(5)

    last_row = ip_spreadsheet.get_last_row('{}!A:A'.format(current_year))
    ip_address = ip_spreadsheet.read_ip('{}!C{}'.format(current_year, last_row))

    print('IP Address: {}'.format(ip_address))

    # RSYNC process
    rsync_options = rsync_options.split()
    process_args = ['rsync', '-e', 
                    "ssh -i {} -p {}".format(rsync_key_path, rsync_port),
                    rsync_source,
                    '{}@{}:{}'.format(rsync_user, ip_address, rsync_dest)]
    # Insert rsync_options into arguments list
    process_args[1:1] = rsync_options
    subprocess.run(process_args)



if __name__ == '__main__':
    # Run codes
    main()