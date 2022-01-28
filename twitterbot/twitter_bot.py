# ##windows
# # BASE_DIR = os.getcwd()
# # BASE_DIR = BASE_DIR.split("\\")[:-1]
# # BASE_DIR = "\\".join(BASE_DIR)
# # sys.path.append(BASE_DIR)


# ##linux
# # BASE_DIR = os.getcwd()
# # sys.path.append(BASE_DIR)

# import tweepy
# from pymongo import MongoClient
# from datetime import datetime, timedelta

# from bot_content_service.tasks.content import celery_content_save_to_db
# from bot_accounts_service.tasks.account import celery_account_save_to_db

# from mongodb.mongo_util import (
#     get_record_details, save_to_mongo_db
#         )
# from mongodb.notify_slack import notify_slack

# from init_twit_api import tweepy_api

# from config.settings import MONGO_URL
# from config.settings import TEXT_REPLY
# from config.settings import SLACK_WEBHOOK

# search_date = datetime.now() + timedelta(0)


# def connect_mongo_db():
#     client = MongoClient(MONGO_URL)
#     db = client.blov_twit_bot
#     collection = db.tweet_data

#     return collection


# def bot_caller_dict_func(item):
#     _dict = {           
#             "name": item['user']['name'],
#             "handle": item['user']['screen_name'],
#             "bio": item['user']['description'],
#             "profile_image": item['user']["profile_image_url"],
#             "tag_id": item['id']
#         }

#     return _dict

# def creator_caller_dict_func(creator_data):

#     _dict = {
#             "name": creator_data['name'],
#             "handle": creator_data['screen_name'],
#             "bio": creator_data['description'],
#             "profile_image": creator_data["profile_image_url"]
#             }

#     return _dict


# def content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id):

#     _dict = {
#             "tweet_creator_dict": creator_dict,
#             "bot_caller_dict": bot_caller_dict,
#             "tweet_id": thread_id,
#             "tag_id": tag_id
#             }

#     return _dict


# def process_tweets(item):    
    
#     search_dict = {"tag_id": item['id']}
#     collection =  connect_mongo_db()
#     search_query = get_record_details(search_dict, collection, find_one=True)

#     created_at_datetime = datetime.strftime(datetime.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
#     created_at_datetime = datetime.strptime(created_at_datetime, '%Y-%m-%d %H:%M:%S')


#     bot_caller_dict = bot_caller_dict_func(item)
    

#     if not search_query  and ("generate" in item['text'].lower())  and (search_date - created_at_datetime).days < 1:
    
#         try:
#             print("as reply")
#             ## tweets that were as replies
#             if item['in_reply_to_status_id']:
                
#                 thread_id = str(item['in_reply_to_status_id'])
#                 handle = item['in_reply_to_screen_name']
#                 tweet_url = f"https://twitter.com/{handle}/status/{thread_id}"

#                 tag_id = item['id']
#                 tag_id_name = item['user']['screen_name']

#                 data = {
#                     "tag_id": tag_id,
#                     "tag_id_name": tag_id_name,
#                     "tweet_id": thread_id,
#                     "handle": handle,
#                     "tweet_url": tweet_url,
#                     "type": "reply",
#                     "created_at": created_at_datetime
#                 }
                

#                 creator_data = tweepy_api.get_user(screen_name = handle)._json
                
#                 creator_dict = creator_caller_dict_func(creator_data)

#                 content_dict = content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id)

#                 # collection = connect_mongo_db()
#                 save_to_mongo_db(data, collection)
#                 #tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True)
#                 notify_slack(data, tag_id_name, SLACK_WEBHOOK)
#                 celery_account_save_to_db.apply_async((bot_caller_dict,), queue="account")
#                 celery_account_save_to_db.apply_async((creator_dict,), queue="account")
#                 result = celery_content_save_to_db.apply_async((content_dict,), queue="content")
#                 print(data)
                
#         except Exception as e:
#             print(e)

#         print("---------------------------------------------------------")
#         try:
#             print("as quote")
#             ## tweets that were as quotes
#             if item['quoted_status_id']:
#                 handle = item['quoted_status']['user']['screen_name']
#                 thread_id = str(item['quoted_status_id'])
#                 tweet_url = f"https://twitter.com/{handle}/status/{thread_id}"

#                 tag_id = item['id']
#                 tag_id_name = item['user']['screen_name']
                
#                 data = {
#                         "tag_id": tag_id,
#                         "tag_id_name": tag_id_name,
#                         "tweet_id": thread_id,
#                         "handle": handle,
#                         "tweet_url": tweet_url,
#                         "type": "quote", 
#                         "created_at": created_at_datetime
#                     }

#                 creator_data = tweepy_api.get_user(screen_name = handle)._json
                
#                 creator_dict = creator_caller_dict_func(creator_data)

#                 content_dict = content_dict_func(creator_dict, bot_caller_dict, thread_id, tag_id)

#                 # collection = connect_mongo_db()
#                 save_to_mongo_db(data, collection)
#                 #tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True)
#                 notify_slack(data, tag_id_name, SLACK_WEBHOOK)
#                 celery_account_save_to_db.apply_async((bot_caller_dict,), queue="account")
#                 celery_account_save_to_db.apply_async((creator_dict,), queue="account")
#                 result = celery_content_save_to_db.apply_async((content_dict,), queue="content")
#                 print(data)


#         except Exception as e:
#             print(e)



# def start_twitter_bot():
#     for item in tweepy.Cursor(tweepy_api.mentions_timeline).items(100):

#         item = item._json

#         process_tweets(item)



# #start_twitter_bot()