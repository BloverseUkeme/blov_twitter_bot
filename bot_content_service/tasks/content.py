from twitterbot.app import create_celery_app
from bot_content_service.content_bot import data_from_twitter_bot_to_content_service


celery = create_celery_app()



@celery.task(name="content.celery_content_save_to_db")
def celery_content_save_to_db(data):
    """
    docker container exec -it "container id" bash
    from bot_content_service.tasks.content import celery_content_save_to_db
    result = celery_content_save_to_db.apply_async((data,), queue="content")
    result = celery.send_task('content.celery_content_save_to_db', (data,), queue="content")    
    data = {
            "tweet_creator_dict": {
                                    "name": "ukeme",
                                    "handle": "wilson1",
                                    "bio": "python is cool",
                                    "profile_image": "thisismyface.jpg"
                                },

            "bot_caller_dict": {
                                    "name": "ukeme",
                                    "handle": "WilsonUkeme",
                                    "bio": "python is cool",
                                    "profile_image": "thisismyface.jpg"
            },
            "tweet_id": "1485585947668455427",
            "tag_id": "1466133326641651717"
            }

    """
    response = data_from_twitter_bot_to_content_service(data)
    return {"response": response}



