from flask import Blueprint, jsonify
from flask_restful import Api, Resource

# from bot_accounts_service.resources.account_bot_resources import AccountBot


class Home(Resource):
    def get(self):
        return jsonify({
            "message": "Welcome to Twitter Bot API!-- USERS ACCOUNT"
        })



account_bot = Blueprint(
    "account_bot", __name__
)

api = Api(account_bot)

api.add_resource(Home, '/account_bot')
# api.add_resource(AccountBot, '/accountbot')
