# import requests
# import os
# import json

# # To set your enviornment variables in your terminal run the following line:
# # export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = "AAAAAAAAAAAAAAAAAAAAALD4WQEAAAAAnB1aH%2B5llYZbPwHJecGe31c5rBA%3DnSdePonpRWlM1cwcrnRaVym27578gxqw5wsvshlfevwhKxgcod"#os.environ.get("BEARER_TOKEN")




# def create_url(tweet_id):
#     tweet_fields = "tweet.fields=lang,author_id,conversation_id,text"
#     # Tweet fields are adjustable.
#     # Options include:
#     # attachments, author_id, context_annotations,
#     # conversation_id, created_at, entities, geo, id,
#     # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
#     # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
#     # source, text, and withheld
#     ids = f"ids={tweet_id}"
#     # You can adjust ids to include a single Tweets.
#     # Or you can add to up to 100 comma-separated IDs
#     url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
#     return url


# def bearer_oauth(r):
#     """
#     Method required by bearer token authentication.
#     """

#     r.headers["Authorization"] = f"Bearer {bearer_token}"
#     r.headers["User-Agent"] = "v2TweetLookupPython"
#     return r


# def connect_to_endpoint(url):
#     response = requests.request("GET", url, auth=bearer_oauth)
#     print(response.status_code)
#     if response.status_code != 200:
#         raise Exception(
#             "Request returned an error: {} {}".format(
#                 response.status_code, response.text
#             )
#         )
#     return response.json()


# def start_tweepy_process(tweet_id):
#     url = create_url(tweet_id)
#     json_response = connect_to_endpoint(url)
# #     print(json.dumps(json_response, indent=4, sort_keys=True))
    
#     return json_response

