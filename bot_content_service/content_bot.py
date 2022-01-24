from pymongo import MongoClient

from config.settings import MONGO_URL

from mongodb.mongo_util import (
    get_record_details, save_to_mongo_db
)

from bot_analysis_service.analysis_bot import start_analysis_bot
from datetime import datetime


# def connect_to_analysis_service(data):

#     payload = json.dumps(data)
    
#     headers = {
#       'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", ANALYSIS_SERVICE_URL, headers=headers, data=payload)
#     print(response.status_code)
#     print(response.text)



def remove_object_id(record_list):
    if type(record_list) == dict:
        record_list.pop('_id', None)
    elif type(record_list) == list:
        [rec.pop('_id', None) for rec in record_list]
    else:
        record_list = list(record_list)
        [rec.pop('_id', None) for rec in record_list]
    
    return record_list


def data_from_twitter_bot_to_content_service(data):
    content_started_at = datetime.now()
    print(content_started_at)

    search_dict = {"tag_id": data['tag_id']}
    
    client = MongoClient(MONGO_URL)
    db = client.blov_twit_content
    collection = db.bot_tweets

    search_query = get_record_details(search_dict, collection, find_one=True)

    if not search_query:
        save_to_mongo_db(data, collection)

        data = remove_object_id(data)
        print(data)
        start_analysis_bot(content_started_at, data)
        

        # print(f"The process too {content_ended_at - content_started_at}")



def listen_from_analysis_service(analysed=False):
    return analysed


def listen_from_response_service(responded=False):
    content_ended_at = datetime.now()
    return responded, content_ended_at
