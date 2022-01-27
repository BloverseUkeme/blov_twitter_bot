import requests
import json
import sys


def notify_slack(data, handle, SLACK_WEBHOOK):
    """
        This sends the content_dict/ data to a slack channel
        data = {
            "tweet_url": "https://twitter.com/bloversebot/status/1486723516909035532",
            "tag_id": 12345678899,

        }
    """

    url =  SLACK_WEBHOOK
    
    message = (f'{data}')
    title = (f"New Incoming Message : {handle} :zap:")
    
    slack_data = {
        "username": f'{handle}',
        "attachments": [
            {
                "color":  "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
        
    return None


# handle = "wilsonukeme"
# data = {
#     "tweet_url": "https://twitter.com/bloversebot/status/1486723516909035532",
#     "tag_id": "12345678899",

# }
# notify_slack(data, handle, SLACK_WEBHOOK)