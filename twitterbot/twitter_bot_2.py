import re
import requests
from datetime import datetime
import tweepy 
import json
from time import sleep
from uuid import uuid4

from mongodb.mongo_util import (
    save_to_mongo_db, connect_to_mongo_db
        )

from config.settings import MONGO_URL
from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from config.settings import SLACK_WEBHOOK
from config.settings import CONTENT_SERVICE_URL
from mongodb.notify_slack import notify_slack
# from blov_twitter.twitterbot.app import create_celery_app

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)



def bot_caller_dict_func(status):
    _dict = {           
            "name": status['user']['name'],
            "handle": status['user']['screen_name'],
            "bio": status['user']['description'],
            "profile_image": status['user']['profile_image_url'],
            "tag_id": status['id']
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


# def content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id):

#     _dict = {
#             "tweet_creator_dict": creator_dict['creator_dict'],
#             "bot_caller_dict": bot_caller_dict['bot_caller_dict'],
#             "tweet_id": thread_id,
#             "tag_id": tag_id
#             }
#     return _dict


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


def cleanup_tweet(tweet, twitter_handle, num_reply=0):
    """
    This function takes in a tweet and then cleans it up by removing non alphanumericals etc
    """
    try:
        tweet_tokens = tweet.split()[num_reply:] # we ignore the first token which will always be the handle
        text_list = []
        for token in tweet_tokens:
            temp = ''.join([i for i in token if (i.isalpha() or (i in ['.',',', '..', '…', ':', ';', '?', '"', '-', '(', ')']) or i.isdigit())])        
            if '#' not in temp:
                if twitter_handle not in temp:
                    text_list.append(temp.strip())

        tweet_text = ' '.join(text_list)
        tweet_text = re.sub(r"http\S+", "", tweet_text)
        tweet_text = tweet_text.strip()
    except Exception as e:
        print(e)
    return tweet_text


def get_thread(tweet_id):
    ### checks if its a single tweet or a thread
    tweet_ids = []
    tweet_id = [tweet_id]
    return tweet_id


def process_tweet_status(tweet_id):
    
    tweet_status = tweepy_api.get_status(tweet_id, tweet_mode="extended")._json
    
    handle = tweet_status['user']['screen_name']
    
    try:
        language = tweet_status['lang']
    except:
        language = "NA"
        
    try:
        created_at = tweet_status['created_at']
        created_at = datetime.strftime(datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
        # created_at_datetime = datetime.strptime(created_at_datetime, '%Y-%m-%d %H:%M:%S')
    except:
        created_at = "NA"
        
    try:
        tweet = tweet_status['full_text']
        tweet = cleanup_tweet(tweet, handle)
    except:
        tweet = "NA"
    
    try:
        quote_tweet_url = tweet_status['quoted_status']['entities']['urls'][0]['expanded_url']
    except:
        quote_tweet_url = "NA"

    try:
        urls = tweet_status['entities']['urls'][0]["expanded_url"]
        if ("twitter.com" in urls) and ("status" in urls):
            urls = []
    except:
        urls = []
        
    try:
        images = [item['media_url_https'] for item in tweet_status['extended_entities']['media']]
    except:
        images = []
        
    try:  
        is_video = tweet_status['extended_entities']['media'][0]['type']
        if is_video == "video":
            video = "Yes"
        else:
            video = "No"
    except:
        video = "No"
        
    try:
        video_url = tweet_status['extended_entities']['media'][0]['video_info']['variants'][0]['url']
    except:
        video_url = []
    
    
    data_dict = {
        "language": language,
        "created_at": created_at,
        "tweet": tweet,
        "quote_tweet_url": quote_tweet_url,
        "urls": [urls],
        "images": images,
        "video": video,
        "video_url": video_url
    } 
    return data_dict


def generate_tweet_info(tweet_ids):
    tweet_infos = []
    for tweet_id in tweet_ids:
        data_dict = process_tweet_status(tweet_id)

        tweet_info = {
                "id": tweet_id,
                "created_at": data_dict['created_at'],
                "language": data_dict['language'],
                "tweet_text": data_dict['tweet'],
                "quote_tweet_url" : data_dict['quote_tweet_url'],
                "tweet_urls": data_dict['urls'],
                "tweet_image_urls": data_dict['images'],
                "tweet_video_urls": data_dict['video_url']
                }
        tweet_infos.append(tweet_info)
    return tweet_infos

def process_content_metadata(tag_id, tweet_id, creator_dict, bot_caller_dict):
    content_started_at = datetime.now()
    content_started_at = datetime.strftime(content_started_at, '%Y-%m-%d %H:%M:%S.%f')

    tweet_ids = get_thread(tweet_id)
    tweet_infos = generate_tweet_info(tweet_ids)

    content_metadata = {
            "content_id": str(uuid4()),
            "content_type" : "Twitter Status",
            "tag_id": tag_id,
            "tweet_id": tweet_id,
            "tweet_creator" : creator_dict,
            "bot_caller": bot_caller_dict,
            "content_started_at" : content_started_at,
            
            "tweet_info": tweet_infos,
            "status":"PENDING",
            "video_url":"",
            "note": ""
        }
    return content_metadata




class MyStreamListener(tweepy.Stream):
    
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweepy_api):
        super().__init__(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def on_data(self, status):
    
        status = json.loads(status.decode('utf-8'))
        collection =  connect_to_mongo_db("blov_twit_bot", "tweet_data", MONGO_URL)

        bot_caller_dict = bot_caller_dict_func(status)

        
        try:
            ## as reply
            if status['in_reply_to_status_id']:
                try:
                    
                    tweet_id, tag_id, tag_id_name, handle, data = tweet_tags_as_reply(status)
                    
                    creator_data = tweepy_api.get_user(screen_name = handle)._json
                    creator_dict = creator_caller_dict_func(creator_data)
                    
                    # celery_content_save_to_db.apply_async((content_dict,), queue="content")
                    # data_dict = process_tweet_status(tweet_id)
                    content_metadata = process_content_metadata(tag_id, tweet_id, creator_dict, bot_caller_dict)
                    
                    connect_to_content_service(content_metadata)
                    save_to_mongo_db(data, collection)
                    notify_slack(data, tag_id_name, SLACK_WEBHOOK)
                    print(data)
                except Exception as e:
                    print(e)
                    
            ## as quote
            elif status['is_quote_status']:
                try:
                    quote_id, tag_id, tag_id_name, handle, data = tweet_tags_as_quote(status)

                    creator_data = tweepy_api.get_user(screen_name = handle)._json
                    creator_dict = creator_caller_dict_func(creator_data)
                    

                    # celery_content_save_to_db.apply_async((content_dict,), queue="content")
                    # celery.send_task('content.celery_account_save_to_db', (content_dict,), queue="content")
                    # data_dict = process_tweet_status(quote_id)
                    content_metadata = process_content_metadata(tag_id, quote_id, creator_dict, bot_caller_dict)
                    
                    connect_to_content_service(content_metadata)
                    save_to_mongo_db(data, collection)
                    notify_slack(data, tag_id_name, SLACK_WEBHOOK)

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
    
    def on_limit(self,status):
        print ("Rate Limit Exceeded, Sleep for 15 Mins")
        sleep(15 * 60)
        return True


def connect_to_content_service( data):

    payload = json.dumps(data)
    
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", CONTENT_SERVICE_URL, headers=headers, data=payload)

    print(response.text)



def start_twitter_bot():
    twitterStream = MyStreamListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweepy_api)
    
    try:
        print('Start streaming.')
        twitterStream.filter(track=["@bloversebot generate"])
    except KeyboardInterrupt:
        print("Stopped.")
    # finally:
    #     print('Done.')
    #     twitterStream.disconnect()


