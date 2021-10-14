import os

from dotenv import load_dotenv

load_dotenv()


# dev/pod
OPERATION = os.getenv("OPERATION")

# redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
