import os
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

# from contentbot.resources.content_bot_resources import ContentBot


class Home(Resource):
    def get(self):
        return jsonify({
            "message": "Welcome to Twitter Bot API!-- CONTENT SERVICE "
        })



content_bot = Blueprint(
    "content_bot", __name__
)


api = Api(content_bot)

api.add_resource(Home, '/')
# api.add_resource(ContentBot, '/contentbot')
