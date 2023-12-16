import os

DATABASE: str = os.environ["POSTGRES_DB"]
USER: str = os.environ["POSTGRES_USER"]
PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
HOST: str = os.environ["POSTGRES_HOST"]
PORT: str = os.environ["POSTGRES_PORT"]