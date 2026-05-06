import os
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
DB_USERNAME = os.environ['POSTGRESQL_USERNAME']
DB_NAME = os.environ['POSTGRESQL_DB_FRCDATASCIENCE']

@contextmanager
def get_connection():
    with psycopg.connect(
        host = '127.0.0.1',
        port = 5432,
        dbname = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
    ) as conn:
        yield conn