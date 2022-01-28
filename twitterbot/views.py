import imp
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from twitterbot.resources.twitter_bot_resources import TwitterBot


class Home(Resource):
    def get(self):
        return jsonify({
            "message": "Welcome to Twitter Bot API!"
        })



twitter_bot = Blueprint(
    "bot", __name__
)

api = Api(twitter_bot)

api.add_resource(Home, '/')
api.add_resource(TwitterBot, "/start_bot")