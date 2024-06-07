import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.environ.get("DOCKER_HOST")
POSTGRES_DB = os.environ.get("DOCKER_DB")
POSTGRES_USER = os.environ.get("DOCKER_USER")
POSTGRES_PASSWORD = os.environ.get("DOCKER_PASSWORD")
