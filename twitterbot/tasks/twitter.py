from twitterbot.app import create_celery_app
from twitterbot.twitter_bot_2 import start_twitter_bot


celery = create_celery_app()



@celery.task()
def celery_start_twitter_bot():
    """
    docker container exec -it "container id" bash
    from twitterbot.tasks.twitter import celery_start_twitter_bot
    result = celery_start_twitter_bot.apply_async((data,), queue="twitter")
    result = celery.send_task('twitter.celery_start_twitter_bot', (data,), queue="twitter")    

    """
    response = start_twitter_bot()
    return {"response": response}



