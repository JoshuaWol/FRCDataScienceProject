import os
from contextlib import contextmanager

from sqlalchemy import create_engine
import psycopg
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
DB_USERNAME = os.environ['POSTGRESQL_USERNAME']
DB_NAME = os.environ['POSTGRESQL_DB_FRCDATASCIENCE']
print(DB_USERNAME)

ENGINE = create_engine(
    f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}"
    f"@127.0.0.1:5432/{DB_NAME}",
    pool_pre_ping=True,   # auto-handles dropped connections
)

@contextmanager
def get_psycopg_connection():
    with psycopg.connect(
        host = '127.0.0.1',
        port = 5432,
        dbname = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
    ) as conn:
        yield conn


@contextmanager
def get_sqlachemy_connection():
    with ENGINE.begin() as conn:
        yield conn

    