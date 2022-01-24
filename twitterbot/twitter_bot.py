import sys
import os

BASE_DIR = os.getcwd()
BASE_DIR = BASE_DIR.split("\\")[:-1]
BASE_DIR = "\\".join(BASE_DIR)
sys.path.append(BASE_DIR)



from twitterbot.app import create_celery_app

celery = create_celery_app()



import tweepy
from pymongo import MongoClient
from datetime import datetime, timedelta


from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from config.settings import MONGO_URL
from config.settings import TEXT_REPLY

from bot_content_service.content_bot import data_from_twitter_bot_to_content_service
from bot_accounts_service.account_bot import save_user_to_db

# from bot_content_service import content_bot #import data_from_twitter_bot_to_content_service
# from ..bot_accounts_service.account_bot import save_user_to_db

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
)



client = MongoClient(MONGO_URL)
db = client.blov_twit_bot
collection = db.tweet_data

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)

search_date = datetime.now() + timedelta(0)




def bot_caller_dict_func(item):
    _dict = {           
            "name": item['user']['name'],
            "handle": item['user']['screen_name'],
            "bio": item['user']['description'],
            "profile_image": item['user']["profile_image_url"],
            "tag_id": item['id'],
            "status": "active"
        }

    return _dict

def creator_caller_dict_func(creator_data):

    _dict = {
            "name": creator_data['name'],
            "handle": creator_data['screen_name'],
            "bio": creator_data['description'],
            "profile_image": creator_data["profile_image_url"]
            }

    return _dict


def content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id):

    _dict = {
            "tweet_creator_dict": creator_dict,
            "bot_caller_dict": bot_caller_dict,
            "tweet_id": thread_id,
            "tag_id": tag_id
            }

    return _dict


def process_tweets(item):    
    
    search_dict = {"tag_id": item['id']}
    search_query = get_record_details(search_dict, collection, find_one=True)

    created_at_datetime = datetime.strftime(datetime.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    created_at_datetime = datetime.strptime(created_at_datetime, '%Y-%m-%d %H:%M:%S')


    bot_caller_dict = bot_caller_dict_func(item)
    

    if search_query == None and ("generate" in item['text'].lower())  and (search_date - created_at_datetime).days < 1:
    
        try:
            print("as reply")
            ## tweets that were as replies
            if item['in_reply_to_status_id']:
                
                thread_id = str(item['in_reply_to_status_id'])
                handle = item['in_reply_to_screen_name']
                tweet_url = f"https://twitter.com/{handle}/status/{thread_id}"

                tag_id = item['id']
                tag_id_name = item['user']['screen_name']

                data = {
                    "tag_id": tag_id,
                    "tag_id_name": tag_id_name,
                    "tweet_id": thread_id,
                    "handle": handle,
                    "tweet_url": tweet_url,
                    "type": "reply",
                    "created_at": created_at_datetime
                }
                

                creator_data = tweepy_api.get_user(screen_name = handle)._json
                
                creator_dict = creator_caller_dict_func(creator_data)

                content_dict = content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id)


                save_to_mongo_db(data, collection)
                tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True)

                save_user_to_db(bot_caller_dict)
                save_user_to_db(creator_dict)
                result = celery.send_task('content.celery_content_save_to_db', (content_dict,), queue="content")
                # data_from_twitter_bot_to_content_service(content_dict)
                print(data)
                
        except Exception as e:
            print(e)

        print("---------------------------------------------------------")
        try:
            print("as quote")
            ## tweets that were as quotes
            if item['quoted_status_id']:
                handle = item['quoted_status']['user']['screen_name']
                thread_id = str(item['quoted_status_id'])
                tweet_url = f"https://twitter.com/{handle}/status/{thread_id}"

                tag_id = item['id']
                tag_id_name = item['user']['screen_name']
                
                data = {
                        "tag_id": tag_id,
                        "tag_id_name": tag_id_name,
                        "tweet_id": thread_id,
                        "handle": handle,
                        "tweet_url": tweet_url,
                        "type": "quote", 
                        "created_at": created_at_datetime
                    }

                creator_data = tweepy_api.get_user(screen_name = handle)._json
                
                creator_dict = creator_caller_dict_func(creator_data)

                content_dict = content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id)


                save_to_mongo_db(data, collection)
                tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True)

                save_user_to_db(bot_caller_dict)
                save_user_to_db(creator_dict)
                result = celery.send_task('content.celery_content_save_to_db', (content_dict,), queue="content")
                # data_from_twitter_bot_to_content_service(content_dict)
                print(data)


        except Exception as e:
            print(e)



def start_twitter_bot():
    for item in tweepy.Cursor(tweepy_api.mentions_timeline).items(100):

        item = item._json

        process_tweets(item)



start_twitter_bot()