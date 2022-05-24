from __future__ import print_function
from config import host, user, password, db_name, port
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import psycopg2
from get_dollar_exchange_rate import get_dollar as gd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1_OKcGaTsd3-gXvZRwJStJ3V0jTBtnbnSz7T1LvyhdMQ'
SAMPLE_RANGE_NAME = 'List1!A2:D51'


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            print('%s, %s, %s, %s' % (row[0], row[1], row[2], row[3]))

    except HttpError as err:
        print(err)

    connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

    pricelistdollars = []
    for row in values:
        pricelistdollars.append(row[2])

    dollar_rate = int(gd())
    pricelistrubles = [int(num) * dollar_rate for num in pricelistdollars]

    print(pricelistdollars)
    print(pricelistrubles)

    with connection.cursor() as cursor:
        for row in values:
            cursor.execute("INSERT INTO list1 (№, order_number, price_dollars, delivery_time) VALUES (%s, %s, %s, %s)", (row[0], row[1], row[2], row[3]))
        connection.commit()

    print ("[INFO] Data was succesfully inserted")


if __name__ == '__main__':
    main()
