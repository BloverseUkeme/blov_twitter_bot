import requests
import json

url = "http://localhost:8002/contentbot"


data = {
  "content_type": "Twitter Status",
  "tag_id": "1506964511475044367",
  "tweet_id": "1506964511475044367",
  "tweet_creator": {
    "name": "ukeme",
    "handle": "wilsonukeme",
    "bio": "this is it",
    "profile_image": "image.png"
  },
  "bot_caller": {
    "name": "ukeme",
    "handle": "wilsonukeme",
    "bio": "this is it",
    "profile_image": "image.png"
  },
  "tweet_info": {
    "id": "1506964511475044367",
    "created_at": "data_dict['created_at']",
    "language": "data_dict['language']",
    "tweet_text": "data_dict['tweet']",
    "quote_tweet_url": "data_dict['quote_tweet_url']",
    "tweet_urls": "data_dict['urls']",
    "tweet_image_urls ": "data_dict['images']",
    "tweet_video_urls ": "data_dict['video_url']"
  }
}


payload = json.dumps(data)
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
