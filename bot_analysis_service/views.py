import os
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

# from analysisbot.resources.analysis_bot_resources import AnalysisBot


class Home(Resource):
    def get(self):
        return jsonify({
            "message": "Welcome to Twitter Bot API! - ANALYSIS SERVICE"
        })



analysis_bot = Blueprint(
    "analysis_bot", __name__
        )




api = Api(analysis_bot)

api.add_resource(Home, '/')
# api.add_resource(AnalysisBot, '/analysisbot')
