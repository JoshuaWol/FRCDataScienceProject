from contextlib import contextmanager


from sqlalchemy import create_engine
import psycopg


from config import DB_USERNAME, DB_PASSWORD, DB_NAME


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
def get_sqlalchemy_connection():
    with ENGINE.begin() as conn:
        yield conn

    