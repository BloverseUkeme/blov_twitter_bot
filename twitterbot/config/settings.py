from decouple import config as env_config

DEBUG = True
MONGO_URL = env_config("MONGO_URL")

CONSUMER_KEY = env_config("CONSUMER_KEY")
CONSUMER_SECRET = env_config("CONSUMER_SECRET")
ACCESS_TOKEN = env_config("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = env_config("ACCESS_TOKEN_SECRET")


TEXT_REPLY = "Seen. Your Video is being processed and the Link will be sent here"

CELERY_BROKER_URL = env_config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env_config("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_CREATE_MISSING_QUEUES = True
CELERY_REDIS_MAX_CONNECTIONS = 15
CELERY_IGNORE_RESULT=True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED=True


## defining queus, exchanges and routes
CELERY_QUEUES = {
        "account": {
            "exchange": "account",
            "exchange_type": "topic",
            "binding_key": "account.#"
        },

        "content": {
            "exchange": "content",
            "exchange_type": "topic",
            "binding_key": "content.#"
        },

        "analysis": {
            "exchange": "analysis",
            "exchange_type": "topic",
            "binding_key": "analysis.#"
        }
}

