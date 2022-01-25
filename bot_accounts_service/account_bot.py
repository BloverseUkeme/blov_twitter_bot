from pymongo import MongoClient
from config.settings import MONGO_URL

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
)


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
