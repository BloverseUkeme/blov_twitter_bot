from decouple import config as env_config

DEBUG = True
MONGO_URL = env_config("MONGO_URL")
CONSUMER_KEY = env_config("CONSUMER_KEY")
CONSUMER_SECRET = env_config("CONSUMER_SECRET")
ACCESS_TOKEN = env_config("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = env_config("ACCESS_TOKEN_SECRET")
CONTENT_SERVICE_URL = env_config("CONTENT_SERVICE_URL")
ACCOUNT_SERVICE_URL = env_config("ACCOUNT_SERVICE_URL")

TEXT_REPLY = "Seen. Your Video is being processed and the Link will be sent here"

