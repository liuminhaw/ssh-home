# -*- conding: UTF-8 -*-

# Standard library imports
from pprint import pprint

# Third party library imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request 


class IpSheet():
    
    def __init__(self, credential, spreadsheet_id):
        """
        Input params:
            credential - Credential to use Google sheet API
            spreadsheet_id - target spreadsheet id
        """
        self.service = build('sheets', 'v4', credentials=credential)
        self.id = spreadsheet_id

    def find_sheet_id(self, sheet_name):
        """
        Get sheetId from given sheet_name
        Return:
            sheetId - If matches to sheet_name is found
            -1 - If no matches to sheet_name is found
        """
        request = self.service.spreadsheets().get(spreadsheetId=self.id)
        response = request.execute()

        for sheet in response['sheets']:
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']
        
        return -1

    def dup_new_sheet(self, source_id, dest_name, dest_id=None, insert_index=0):
        """
        Duplicate new sheet from given sheet source_id
        Return:
            True - Duplicate sheet success
            False - Failed to duplicate sheet
        """
        requests = [
            {
                'duplicateSheet': {
                    'sourceSheetId': source_id,
                    'insertSheetIndex': insert_index,
                    'newSheetId': dest_id,
                    'newSheetName': dest_name
                }
            }
        ]
        body = {
            'requests': requests
        }

        try:
            request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.id, body=body)
            response = request.execute()
        except:
            return False
        else:
            return True

    def get_last_row(self, range):
        """
        Get last row of givenv range
        Return:
            Last row's number
        """
        request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
        response = request.execute()

        return len(response.get('values', []))

    def update_ip(self, range, value):
        """
        Update IP sheet data with record date and time
        Input params:
            range - A1 notation range
            value - list containing desire values
        """
        value_input_option = 'USER_ENTERED'
        value_range_body = {
            'range': range,
            'values': [value]
        }

        request = self.service.spreadsheets().values().update(spreadsheetId=self.id, 
            range=range, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

    def read_ip(self, range):
        """
        Get latest IP address from target sheet
        Input params:
            range - A1 notation range
        Return:
            latest ip address
        """
        request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
        response = request.execute()

        ip_address = response['values'][0][0]
        return ip_address
