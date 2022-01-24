# from flask_restful import Resource
# from flask import request

# from contentbot.content_bot import save_content_to_db

# class ContentBot(Resource):
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

#             result = save_content_to_db(json_data)
    
#             return {
#                 'status': 'success',  
#                 'data': None, 
#                 'message': 'CONTENT Bot successful.'
#             }, 200

#         except Exception as e:
#             return {
#                 'status': 'failed',
#                 'data': None,
#                 'message': str(e)
#             }, 500
            