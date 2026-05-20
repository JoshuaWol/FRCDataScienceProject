import os


from dotenv import load_dotenv

env = os.getenv("APP_ENV", "dev")
load_dotenv(".env") 
load_dotenv(f".env.{env}", override=True)

DATABASE_URL = os.environ['DATABASE_URL']
DB_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
DB_USERNAME = os.environ['POSTGRESQL_USERNAME']
DB_NAME = os.environ['POSTGRESQL_DB_FRCDATASCIENCE']
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
POSTGRESQL_OPTUNA_DB_URL = os.environ['POSTGRESQL_OPTUNA_DB_URL']


IF_EXISTS = 'append'