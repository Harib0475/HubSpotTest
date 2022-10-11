import os
import random
import string
import datetime

from dotenv import load_dotenv

load_dotenv()


def generate_random_data():
    """
        Generate 2 random records for insertion
    """

    results = []
    for i in range(2):
        first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        company = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        email = f'{first_name}.{last_name}@{company}.com'
        results.append({
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        })
    return results


def get_env_variables():
    """
        Get all environment variables
    """

    env_variables = ['CLIENT_SECRET', 'CLIENT_ID', 'REDIRECT_URL', 'CODE', 'DB_URL']
    list = []
    for i, j in os.environ.items():
        if i in env_variables:
            list.append({i: j})
    return list


def set_token_to_env(response):
    """
        Save Access and refresh token in environment for future use
    """

    if response['access_token']:
        list = get_env_variables()
        open('.env', 'w').close()
        with open(".env", "a") as envfile:
            envfile.write(f"ACCESS_TOKEN={response['access_token']}\n")
            envfile.write(f"REFRESH_TOKEN={response['refresh_token']}\n")
            envfile.write(f"EXPIRES_IN={str(response['expires_in'])}\n")
            envfile.write(f"DATETIME={str(datetime.datetime.now())}\n")
            for dict in list:
                for key in dict:
                    envfile.write(f"{key}={dict[key]}\n")
        load_dotenv()
