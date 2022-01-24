from twitterbot.app import create_celery_app
from bot_accounts_service.account_bot import save_user_to_db 

celery = create_celery_app()


@celery.task(name="account.celery_account_save_to_db")
def celery_account_save_to_db(data):
    """
    from bot_accounts_service.tasks.account import celery_account_save_to_db
    result = celery_account_save_to_db.apply_async((data,), queue="account")
    result = celery.send_task('account.celery_account_save_to_db', (data,), queue="account")
    data = {
        "name": "ukeme",
        "handle": "wilson123456",
        "bio": "python is cool",
        "profile_image": "thisismyface.jpg",
        "status": "active"
        }
    """

    response = save_user_to_db(data) 
    return {"response": response}