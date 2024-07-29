import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ELASTIC_USER = os.getenv('ELASTIC_USER')
    ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
    ELASTIC_PORT = os.getenv('ES_PORT')
    ELASTIC_HOST = os.getenv('ES_HOST')


settings = Settings()
