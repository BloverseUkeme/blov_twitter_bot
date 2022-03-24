from datetime import datetime
from pymongo import MongoClient
from config.settings import MONGO_URL, SLACK_WEBHOOK_POT_BOT_USER
from mongodb.notify_slack import notify_slack


client = MongoClient(MONGO_URL)
db = client.potential_bot_users_db
collection = db.potential_bot_users



start_day = datetime.now().replace(hour=0, minute=0)
end_day = datetime.now()

def potential_db_query():

    end_of_day_query = list(collection.find({"date": {"$gte": start_day, "$lte": end_day}}))
    print(end_of_day_query)
    total_query = list(collection.find()) 
    
    data = {
        "todays_total": len(end_of_day_query),
        "grand_total": len(total_query)
    }
    return data

data = potential_db_query()

notify_slack(data, SLACK_WEBHOOK_POT_BOT_USER)