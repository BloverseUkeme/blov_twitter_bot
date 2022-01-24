from twitterbot.app import create_celery_app
from bot_analysis_service.analysis_bot import start_analysis_bot 

celery = create_celery_app()


@celery.task(name="analysis.celery_analysis_save_to_db")
def celery_analysis_save_to_db(content_started_at, data):

    """
    docker container exec -it "container id" bash
    from bot_analysis_service.tasks.analysis import celery_analysis_save_to_db
    result = celery_analysis_save_to_db.apply_async((content_started_at, data), queue="analysis")
    result = celery.send_task('content.celery_analysis_save_to_db', (data,), queue="analysis")    
    data = {
            "tweet_creator_dict": {
                                    "name": "ukeme",
                                    "handle": "wilson1234",
                                    "bio": "python is cool",
                                    "profile_image": "thisismyface.jpg"
                                },

            "bot_caller_dict": {
                                    "name": "ukeme",
                                    "handle": "WilsonUkeme",
                                    "bio": "python is cool",
                                    "profile_image": "thisismyface.jpg"
            },
            "tweet_id": "1484206745748652034",
            "tag_id": "987654321123456789"
            }
    
    """

    response = start_analysis_bot(content_started_at, data) 
    return {"response": response}
