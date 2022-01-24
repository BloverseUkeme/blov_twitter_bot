from pymongo import MongoClient
from config.settings import MONGO_URL
# from twitterbot.twitter_bot import tweepy_api

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
)

# client = MongoClient(MONGO_URL)
# db = client.account_bot
# collection = db.users



def save_user_to_db(data):
    search_dict = {"handle": data['handle']}
    
    client = MongoClient(MONGO_URL)
    db = client.blov_twit_accounts
    collection = db.bot_users

    search_query = get_record_details(search_dict, collection, find_one=True)

    if not search_query:
        save_to_mongo_db(data, collection)
        return "User Added to DB"

    else:
        return "User Already Registered"



# def process_or_reply(data):
#     if data.get("status") == "active":
#         ...
#     else:
#         TEXT_REPLY = "beta testing currently on going."
#         tag_id = data.get('tag_id')
#         tweepy_api.update_status(status = TEXT_REPLY, in_reply_to_status_id = tag_id , auto_populate_reply_metadata=True)



