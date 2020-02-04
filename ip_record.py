# -*- coding:UTF-8 -*-

# Standard library imports
import os, sys
import pickle
from datetime import datetime

# Third party library imports
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Local application imports
from module_pkg import conf_mod
from module_pkg import sheet
from module_pkg import logging_class as logcl

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CONFIG_FILE = ['config.ini']
LOG_DIR = os.path.join(os.getcwd(), 'logs')

logger = logcl.PersonalLog('ip_record', LOG_DIR)

def main():

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
        template = config.template_sheet()
    except conf_mod.NoSectionError as err:
        logging = 'config.ini section error: {}'.format(err)
        logger.info(logging)
        sys.exit(12)
    except conf_mod.NoOptionError as err:
        logging = 'config.ini option error: {}'.format(err)
        logger.info(logging)
        sys.exit(13)

    information = '\nSpreadsheet id: {}\n'.format(spreadsheet_id)
    information += 'Template name: {}\n'.format(template)

    # Credential to use Google sheet API
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    ip_spreadsheet = sheet.IpSheet(creds, spreadsheet_id)

    # Set date data
    current_datetime = datetime.now()
    current_year = current_datetime.strftime('%Y')
    current_date = current_datetime.strftime('%d/%m/%Y')
    current_time = current_datetime.strftime('%H:%M:%S')

    # Get template sheet ID
    template_id = ip_spreadsheet.find_sheet_id(template)
    if template_id == -1:
        logger.info('Template sheet {} not found'.format(template))
        sys.exit(3)
    else:
        information += 'Template ID: {}\n'.format(template_id)
    
    # Duplicate sheet for each year
    worksheet_id = ip_spreadsheet.find_sheet_id(current_year)
    if worksheet_id == -1:
        ip_spreadsheet.dup_new_sheet(template_id, current_year, dest_id=current_year)

    # Add ip record
    last_row = ip_spreadsheet.get_last_row('{}!A:A'.format(current_year))
    #print('Last row: {}'.format(last_row))

    current_ip = public_ip()
    update_range = '{sheet}!A{row}:C{row}'.format(sheet=current_year, row=last_row+1)
    update_values = [current_date, current_time, current_ip]
    #print('Updae range: {}'.format(update_range))

    ip_spreadsheet.update_ip(update_range, update_values)
    information += 'Current IP: {}'.format(current_ip)
    logger.info(information)


def public_ip():
    """
    Find and return public ip address
    Use Amazon AWS endpoint
    """
    return requests.get('https://checkip.amazonaws.com').text.strip()



if __name__ == '__main__':
    main()