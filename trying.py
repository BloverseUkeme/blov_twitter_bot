# # import tweepy
# # from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# # tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)

# # import os
# # # a = os.getcwd() + "/videos/video.mp4"
# # # print(a)


# # def response_service_video(tag_id):
# #     text_cta = "Your Video is ready. Visit ..."
# #     path = os.getcwd() + "/videos/vidd.mp4"
# #     print(path)
# #     upload_result = tweepy_api.media_upload(path)
# #     tweepy_api.update_status(status = text_cta, media_ids = [upload_result.media_id_string], in_reply_to_status_id= tag_id, auto_populate_reply_metadata=True)


# # response_service_video("1486720974443593735")



# import tweepy
# import json

# from config.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)




# class MyStreamListener(tweepy.Stream):
#     def __init__(self, cons_key, cons_secret, token, token_sec):
#         super().__init__(cons_key, cons_secret, token, token_sec)

#     def on_data(self, status):
#         status = json.loads(status.decode('utf-8'))
        

#         print(str(status["id"]) + " tweeted " + status["text"])
#         from datetime import datetime
#         created_at_datetime = status['created_at']

#         created_at_datetime = datetime.strftime(datetime.strptime(created_at_datetime,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

#         print(created_at_datetime)
#         print(type(created_at_datetime))

# twitterStream = MyStreamListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# try:
#     print('Start streaming.')
#     # word = "generate" 
#     # stream.filter(track=["@bloversebot generate"])
#     twitterStream.filter(track=["@bloversebot generate"])

# except KeyboardInterrupt:
#     print("Stopped.")
# # finally:
# #     print('Done.')
# #     twitterStream.disconnect()
