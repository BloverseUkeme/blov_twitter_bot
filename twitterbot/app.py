# from __future__ import absolute_import

from flask import Flask

#views
from twitterbot.views import twitter_bot
from bot_accounts_service.views import account_bot
from bot_content_service.views import content_bot
from bot_analysis_service.views import analysis_bot


from celery import Celery


CELERY_TASK_LIST = [
    "bot_accounts_service.tasks.account",
    "bot_content_service.tasks.content",
    "bot_analysis_service.tasks.analysis",
    "twitterbot.tasks.twitter",
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, 
                    broker=app.config['CELERY_BROKER_URL'],
                    backend_url=app.config["CELERY_RESULT_BACKEND"],
                    include=CELERY_TASK_LIST)

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery



def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)


    app.register_blueprint(twitter_bot)
    app.register_blueprint(account_bot)
    app.register_blueprint(content_bot)
    app.register_blueprint(analysis_bot)


    return app


