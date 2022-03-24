from datetime import datetime, timedelta
import pandas as pd
import tweepy
from functions import twitter_funcs as twt

from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from mongodb.mongo_util import save_to_mongo_db, get_record_details, connect_mongo_db


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)



country_woeid_dict =  {
            "Nigeria": 23424908,
            "USA":23424977,
            "UK" : 23424975,
            "Ghana" : 23424824,
            "Kenya": 23424863,
            "South_Africa": 23424942,
            "India": 23424848,
            "Colombia": 23424787,
            "Mexico": 23424900,
            "Canada": 23424775 }



def process_trend_items(search_term_list):
    trending_df_list = []

    num_tweets = 500
    min_replies = 0
    verified = False

    extraction_day = str(datetime.now().date())
    extraction_time = '%s 00:00:00' % extraction_day

    extraction_time = datetime.strptime(extraction_time, '%Y-%m-%d %H:%M:%S')

    search_date_str = str(extraction_time - timedelta(hours=24))

    for search_term in search_term_list:
        print(search_term)
        results_df = twt.get_tweets_from_search_term(search_term, min_replies, verified, num_tweets, search_date_str)
        trending_df_list.append(results_df)

    # # Combine the tweet dfs 
    trending_tweet_df = pd.concat(trending_df_list)
    trending_tweet_df = trending_tweet_df[trending_tweet_df['language'] == "en"]
    
    return trending_tweet_df



def process_trending_tweets(trending_tweet_df):

    relevant_tweeters, relevant_tweet_count, relevant_tweets_df = twt.process_tweets_for_relevance(trending_tweet_df)
    relevant_tweets_df = relevant_tweets_df.sort_values(by=['nlikes'], ascending=False)

    return relevant_tweeters, relevant_tweet_count, relevant_tweets_df


# def process_non_mentions(relevant_tweets_df):
#     conv_ids = relevant_tweets_df['conversation_id']
#     tweet_ids = relevant_tweets_df['id']
    
#     non_mention_df = relevant_tweets_df[conv_ids == tweet_ids]

#     percent_non_mention = (len(non_mention_df)/len(relevant_tweets_df)) * 100

#     return percent_non_mention

def process_potential_bot_users_func(trending_relevant_tweeters):

    try:
        for i in range(len(trending_relevant_tweeters)):
            twitter_handle = trending_relevant_tweeters[i]
            print(twitter_handle)

            collection = connect_mongo_db("potential_bot_users_db", "potential_bot_users")
            search_query = {"twitter_handle": twitter_handle}
            processed_query = get_record_details(search_query, collection)
            # Check if the twitter handle has already been processed before

            if not processed_query: #== False:
                # Check if the twitter handle is a potential bot user
                potential_bot_user_flag, potential_bot_user_dict = twt.process_potential_bot_user(twitter_handle)
                if len(potential_bot_user_dict) > 1:
                    save_to_mongo_db(potential_bot_user_dict, collection)

    except Exception as e:
        print(e)



def get_potential_bot_users():
    for country, woeid in list(country_woeid_dict.items()):
        print(country)
        trends_result =  tweepy_api.get_place_trends(woeid)
        trends_result_df = pd.DataFrame(trends_result[0]['trends'])
        trends_result_df = trends_result_df.sort_values("tweet_volume", ascending=False)[:10]
        
        search_term_list = trends_result_df['name'].tolist()
        print(search_term_list)
        trending_tweet_df = process_trend_items(search_term_list)
        relevant_tweeters, relevant_tweet_count, relevant_tweets_df = process_trending_tweets(trending_tweet_df)
        
        trending_relevant_tweeters = list(relevant_tweets_df['username'])
        print(len(trending_relevant_tweeters))

        process_potential_bot_users_func(relevant_tweeters)

get_potential_bot_users()