# from flask_restful import Resource
# from analysisbot.analysis_bot import start_analysis_bot
# from flask import request



# class AnalysisBot(Resource):
#     def post(self):
#         try:
#             json_data = request.get_json()
            
#             req_fields = ['tweet_creator_dict', "bot_caller_dict", "tweet_id", "tag_id"]

#             for field in req_fields:
#                 if field not in json_data:
#                     return {
#                        'status': 'failed',
#                        'data': None,
#                        'message': field + ' is required'
#                     }, 400
#                 elif json_data[field] == '':
#                     return {
#                        'status': 'failed',
#                        'data': None,
#                        'message': field + ' cannot be empty'
#                     }, 400
#                 else:
#                     pass


#             result = start_analysis_bot(json_data)
#             return {
#                 'status': 'success',  
#                 'data': result, 
#                 'message': 'Analysis Bot successful.'
#             }, 200

#         except Exception as e:
#             return {
#                 'status': 'failed',
#                 'data': None,
#                 'message': str(e)
#             }, 500
            