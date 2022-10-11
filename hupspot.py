import json
import os
import time
import datetime
import requests
from datetime import datetime as dt

from dotenv import load_dotenv

from helper import set_token_to_env

load_dotenv()


class HubSpot:

    def __init__(self):
        """
            Establish a connection with hubspot
        """

        self.client_secret = os.getenv('CLIENT_SECRET')
        self.client_id = os.getenv('CLIENT_ID')
        self.redirect_url = os.getenv('REDIRECT_URL')
        self.code = os.getenv('CODE')
        self.auth_token_url = 'https://api.hubapi.com/oauth/v1/token'
        try:
            if not os.getenv('ACCESS_TOKEN'):
                self.getAccessToken()
        except Exception as e:
            print(e)

    def getAccessToken(self):
        """
            Get Access token from hubspot using code and secret keys
        """

        try:
            data = {'grant_type': 'authorization_code', 'client_id': self.client_id,
                    'client_secret': self.client_secret, 'redirect_uri': self.redirect_url,
                    'code': self.code}
            headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
            response = requests.post(url=self.auth_token_url, headers=headers, data=data)
            set_token_to_env(response=response.json())
        except Exception as e:
            print(e)

    class Decorators():
        @staticmethod
        def refreshToken(decorated):
            """
                Refresh Access token using refresh token and secret keys
            """

            def wrapper(*args, **kwargs):
                if os.getenv('DATETIME'):
                    prev_datetime = dt.fromtimestamp(
                        time.mktime(time.strptime(os.getenv('DATETIME'), '%Y-%m-%d %H:%M:%S.%f')))
                    curr_datetime = datetime.datetime.now()
                    diff = curr_datetime - prev_datetime
                    if diff.seconds >= 10:
                        try:
                            data = {'grant_type': 'refresh_token', 'client_id': 'eb890419-5660-4b46-9cf7-6457a8ad28b6',
                                    'client_secret': '7f5db265-c6fb-45d2-9cbb-8776470950b2',
                                    'refresh_token': os.getenv('REFRESH_TOKEN')}
                            headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
                            url = 'https://api.hubapi.com/oauth/v1/token'
                            response = requests.post(url=url, headers=headers, data=data)
                            set_token_to_env(response.json())
                        except Exception as e:
                            print(e)
                return decorated(*args, **kwargs)

            return wrapper

    @Decorators.refreshToken
    def create_or_update_contact(self, contact):
        """
            Create Or Update Records in Hubspot
        """

        url = f'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{contact["email"]}'
        headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {os.getenv('ACCESS_TOKEN')}"}
        data = json.dumps({
            "properties": [
                {
                    "property": "email",
                    "value": contact['email']
                },
                {
                    "property": "firstname",
                    "value": contact['first_name']
                },
                {
                    "property": "lastname",
                    "value": contact['last_name']
                },
            ]
        })
        response = requests.post(data=data, url=url, headers=headers)
        return response
