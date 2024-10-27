import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

ORIGINS = os.environ.get('ORIGINS').split(' ')

DEFAULT_PHONE = '+79999999999'

REFRESH_TTL_DAYS = 30
ACCESS_TTL_MINUTES = 60

SHA_KEY = os.environ.get('SHA_KEY').encode()
SALT = os.environ.get('SALT').encode()
