import requests
import json
import sys
from datetime import datetime


def notify_slack(data, SLACK_WEBHOOK):
    """
        This sends the content_dict/ data to a slack channel
        
        data = {'todays_total': 0, 'grand_total': 88}
        
    """
    
    report_date = datetime.now()
    
    
    url =  SLACK_WEBHOOK
    
    message = (f'{data}')
    title = (f"New Incoming Message : {report_date} :zap:")
    
    slack_data = {
        "username": f'{report_date}',
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

