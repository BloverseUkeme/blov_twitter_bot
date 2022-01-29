from pymongo import MongoClient
from config.settings import MONGO_URL

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db, update_record
)


from init_twit_api import tweepy_api

def save_user_to_db(data):
    search_dict = {"handle": data['handle']}
    
    client = MongoClient(MONGO_URL)
    db = client.blov_twit_accounts
    collection = db.bot_users

    search_query = get_record_details(search_dict, collection, find_one=True)
    try:

        if "active" in data.get('status'):
            search_query['status'] = "active" 
        

        new_values = {"$set" : search_query}
        update_record(collection, search_dict, new_values)
    except Exception as e:
        print(e)


    if not search_query:
        save_to_mongo_db(data, collection)
        return "User Added to DB"

    else:
        return "User Already Registered"




# def handle_dict_func(handle_data):

#     _dict = {
#             "name": handle_data['name'],
#             "handle": handle_data['screen_name'],
#             "bio": handle_data['description'],
#             "profile_image": handle_data["profile_image_url"],
#             "status": "active"
#             }

#     return _dict



# def save_handle_to_db(handle):

#     try:
#         handle_data = tweepy_api.get_user(screen_name = handle)._json
#     except Exception as e:
#         print(e)
#         return {"response":"Username not found"}

#     handle_dict = handle_dict_func(handle_data)
    
#     return save_user_to_db(handle_dict)
