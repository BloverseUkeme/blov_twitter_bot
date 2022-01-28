
from datetime import datetime
import tweepy 
import json

from pymongo import MongoClient
from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
        )
from config.settings import MONGO_URL

from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from config.settings import SLACK_WEBHOOK
from mongodb.notify_slack import notify_slack


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)


def connect_mongo_db():
    client = MongoClient(MONGO_URL)
    db = client.blov_twit_bot
    collection = db.tweet_data

    return collection



def bot_caller_dict_func(status):
    _dict = {           
            "name": status['user']['name'],
            "handle": status['user']['screen_name'],
            "bio": status['user']['description'],
            "profile_image": status['user']['profile_image_url'],
            "tag_id": status['id'],
            "tweet_creator": "no"
        }

    return _dict



def creator_caller_dict_func(creator_data):

    _dict = {
            "name": creator_data['name'],
            "handle": creator_data['screen_name'],
            "bio": creator_data['description'],
            "profile_image": creator_data["profile_image_url"],
            "tweet_creator": "yes"
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


def tweet_tags_as_reply(status):

    created_at_datetime = status['created_at']
    created_at_datetime = datetime.strftime(datetime.strptime(created_at_datetime,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

    tweet_id = str(status['in_reply_to_status_id'])
    handle = status["in_reply_to_screen_name"]
    tweet_url = f"https://twitter.com/{handle}/status/{tweet_id}"
    tag_id = status["id"]
    tag_id_name = status['user']['screen_name']

    data = {
            "tag_id": tag_id,
            "tag_id_name": tag_id_name,
            "tweet_id": tweet_id,
            "handle": handle,
            "tweet_url": tweet_url,
            "type": "reply",
            "created_at": created_at_datetime
        }

    return tweet_id, tag_id, tag_id_name, handle, data



def tweet_tags_as_quote(status):
    
    created_at_datetime = status['created_at']
    created_at_datetime = datetime.strftime(datetime.strptime(created_at_datetime,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    
    quote_id = str(status['quoted_status_id'])
    handle = status['quoted_status']['user']['screen_name']
    tweet_url = f"https://twitter.com/{handle}/status/{quote_id}"

    tag_id = status["id"]
    tag_id_name = status['user']['screen_name']
    
    data = {
            "tag_id": tag_id,
            "tag_id_name": tag_id_name,
            "tweet_id": quote_id,
            "handle": handle,
            "tweet_url": tweet_url,
            "type": "quote", 
            "created_at": created_at_datetime
        }

    return quote_id, tag_id, tag_id_name, handle, data


class MyStreamListener(tweepy.Stream):
    
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweepy_api):
        super().__init__(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def on_data(self, status):
        from bot_content_service.tasks.content import celery_content_save_to_db
        from bot_accounts_service.tasks.account import celery_account_save_to_db

        status = json.loads(status.decode('utf-8'))
        collection =  connect_mongo_db()

        bot_caller_dict = bot_caller_dict_func(status)

        
        try:
            ## as reply
            if status['in_reply_to_status_id']:
                try:
                    
                    tweet_id, tag_id, tag_id_name, handle, data = tweet_tags_as_reply(status)
                    
                    creator_data = tweepy_api.get_user(screen_name = handle)._json

                    creator_dict = creator_caller_dict_func(creator_data)
                    
                    content_dict = content_dict_func(creator_dict, bot_caller_dict, tweet_id, tag_id)
                    
                    save_to_mongo_db(data, collection)
                    notify_slack(data, tag_id_name, SLACK_WEBHOOK)

                    celery_account_save_to_db.apply_async((bot_caller_dict,), queue="account")
                    celery_account_save_to_db.apply_async((creator_dict,), queue="account")
                    celery_content_save_to_db.apply_async((content_dict,), queue="content")
                    print(data)
                except Exception as e:
                    print(e)
                    
            ## as quote
            elif status['is_quote_status']:
                try:
                    quote_id, tag_id, tag_id_name, handle, data = tweet_tags_as_quote(status)

                    creator_data = tweepy_api.get_user(screen_name = handle)._json
                
                    creator_dict = creator_caller_dict_func(creator_data)

                    content_dict = content_dict_func(creator_dict, bot_caller_dict, quote_id, tag_id)
                    save_to_mongo_db(data, collection)
                    notify_slack(data, tag_id_name, SLACK_WEBHOOK)

                    celery_account_save_to_db.apply_async((bot_caller_dict,), queue="account")
                    celery_account_save_to_db.apply_async((creator_dict,), queue="account")
                    celery_content_save_to_db.apply_async((content_dict,), queue="content")

                    print(data)

                except Exception as e:
                    print(e)
            else:
                pass
        except Exception as e:
            print(e)
        
    def on_error(self, status_code):
        print(status_code)
        return False


def start_twitter_bot():
    
    twitterStream = MyStreamListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweepy_api)

    try:
        print('Start streaming.')
        # word = "generate" 
        twitterStream.filter(track=["@bloversebot generate"])
    except KeyboardInterrupt:
        print("Stopped.")
    # finally:
    #     print('Done.')
    #     twitterStream.disconnect()