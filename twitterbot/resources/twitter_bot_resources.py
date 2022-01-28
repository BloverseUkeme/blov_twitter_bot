from flask_restful import Resource
from twitterbot.twitter_bot_2 import start_twitter_bot


class TwitterBot(Resource):
    def get(self):
        try:

            result = start_twitter_bot()
            return {
                'status': 'success',
                'data': None, 
                'message': 'Twitter Bot successful.'
            }, 200

        except Exception as e:
            return {
                'status': 'failed',
                'data': None,
                'message': str(e)
            }, 500



