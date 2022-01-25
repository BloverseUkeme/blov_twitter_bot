import re
import os
from pymongo import MongoClient
from datetime import datetime
from init_twit_api import tweepy_api
from config.settings import MONGO_URL

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
)

## fix this later please
# from bot_content_service.content_bot import listen_from_analysis_service, listen_from_response_service




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



def remove_object_id(record_list):
    if type(record_list) == dict:
        record_list.pop('_id', None)
    elif type(record_list) == list:
        [rec.pop('_id', None) for rec in record_list]
    else:
        record_list = list(record_list)
        [rec.pop('_id', None) for rec in record_list]
    
    return record_list


def process_tweet_status(tweet_id):
    
    tweet_status = tweepy_api.get_status(tweet_id)._json
    
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
        tweet = tweet_status['text']
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
        video_url = "NA"
    
    
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



def process_data_status(tweet_status, tag_id, tweet_id, data):

    _dict = {
            "tag_id": tag_id,
            "tweet_id": tweet_id,
            "tweet_creator" : data['tweet_creator_dict'],
            "bot_caller": data['bot_caller_dict'],
            
            "tweet_info": {
                "id": tweet_id,

                "created_at": tweet_status['created_at'],

                "language": tweet_status['language'],

                "tweet_text": tweet_status['tweet'],

                "quote_tweet_url" : tweet_status['quote_tweet_url'],

                "tweet_urls": tweet_status['urls'],

                "tweet_image_urls ": tweet_status['images'],

                "tweet_video_urls ": tweet_status['video_url']
                }
        }
    return _dict


def sort_tweets(data):
    tweet_response_dict = initial_tweet_processing(data)

    return tweet_response_dict


def initial_tweet_processing(data):

    tweet_id = data['tweet_id']
    tag_id = data['tag_id']
    tweet_status = process_tweet_status(tweet_id)
    data_status = process_data_status(tweet_status, tag_id, tweet_id, data)

    print(data_status)

    client = MongoClient(MONGO_URL)
    db = client.blov_twit_analysis
    collection = db.analysis_data

    
    search_dict = {"tweet_id": tweet_id}
    search_query = get_record_details(search_dict, collection, find_one=True)

    if not search_query:
        save_to_mongo_db(data_status, collection)


        analysed = listen_from_analysis_service(analysed=True)

        data_status = remove_object_id(data_status)




    tweet_response_dict = {
        "tweet_url": "tweet_url",
        "tweet_text": "tweet_text",
        "cta_url": "cta_url" ,
        "video_url": "video_url",
    }

    return tweet_response_dict



def check_account_service_status(content_started_at, data):
    handle = data['bot_caller_dict']['handle']
    tag_id = data['tag_id']
    print(handle)

    search_dict = {"handle": handle}

    client = MongoClient(MONGO_URL)
    db = client.blov_twit_accounts
    collection1 = db.bot_users

    search_query = get_record_details(search_dict, collection1, find_one=True)

    print(search_query)
    if search_query:
        status = search_query.get('status')
        print(status)
        if status == "active":
            tweet_response_dict = sort_tweets(data)
            print(tweet_response_dict)
            ### respond with tweet_response_dict
            
            response_service_video(tag_id)
            responded, content_ended_at = listen_from_response_service(responded=True)
            print(f"The process too {content_ended_at - content_started_at}")
        else:
            ## respond with cta 
            response_service_text(tag_id)
            responded, content_ended_at = listen_from_response_service(responded=True)
            print(f"The process too {content_ended_at - content_started_at}")
            
    else:
        response_service_text(tag_id)     
        responded, content_ended_at = listen_from_response_service(responded=True)
        print(f"The process too {content_ended_at - content_started_at}")


def listen_from_analysis_service(analysed=False):
    return analysed

def listen_from_response_service(responded=False):
    content_ended_at = datetime.now()
    return responded, content_ended_at

    


def response_service_video(tag_id):
    text_cta = "Your Video is ready. Visit www.bloverse.com"
    path = os.getcwd() + "/videos/vid.mp4"
    print(path)
    upload_result = tweepy_api.media_upload(path)
    tweepy_api.update_status(status = text_cta, media_ids = [upload_result.media_id_string], in_reply_to_status_id= tag_id, auto_populate_reply_metadata=True)


def response_service_text(tag_id):
    TEXT_REPLY = "We are currently in Beta testing. You can register at ##bloversebot_landing_page"
    tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True) 



def start_analysis_bot(content_started_at, data):

    check_account_service_status(content_started_at, data)
