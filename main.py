import requests
import random
import string
from typing import List
from datetime import datetime, timedelta


class Authorization:

    def generate_password(self, length: int = 16) -> str:
        """
         Generate a password of a given `length`.
         """
        result: List[str] = []
        choices = string.printable  # заглавые и строчные буквы, цифры и знаки препинания
        while len(result) < length:
            symbol = random.choice(string.printable)
            result.append(symbol)
        return "".join(result)


    def generate_random_date(self):
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2000, 1, 1)
        t: timedelta = end_date - start_date
        rand_days: int = random.randrange(t.days)
        result = start_date + timedelta(days=rand_days)
        return result.strftime("%Y-%m-%d")


    def register(self, username: str, email: str, password: str) -> None:
        date: str = self.generate_random_date()
        captcha_key: str = input("Please input captcha : ")

        data: dict = {
            'captcha_key': captcha_key,
            'consent': True,
            'date_of_birth': date,
            'email': email,
            'fingerprint': 'null',
            'gift_code_sku_id': None,
            'invite': None,
            'password': password,
            'username': username,
        }

        headers: dict = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }

        response = requests.post('https://discord.com/register', headers=headers, json=data)
        return response

    def get_token(self, email: str, password: str) -> None:
        headers: dict = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Host': 'discord.com',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json',
            'Referer': 'https://discord.com/register',
            'Origin': 'https://discord.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

        data: dict = {
            'email': email,
            'password': password,
        }
        response = requests.post('https://discord.com/api/v6/auth/login',
                                 headers=headers, json=data)
        j_data = response.json()
        print("\nCaptcha finished, grabbing token.\n")
        try:
            return print(j_data['token'])
        except:
            token = "Could not get token."
            return print(token)



if __name__ == "__main__":
    runner = Authorization()
    password = runner.generate_password()
    username = input('Enter your name: ')
    email = input('Enter your email: ')
    runner.register(email, username, password)
    runner.get_token(email, password)

