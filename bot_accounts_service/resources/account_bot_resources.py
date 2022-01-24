# from flask_restful import Resource
# from flask import request
# from bot_accounts_service.account_bot import save_user_to_db


# class AccountBot(Resource):
#     def post(self):
#         try:
            
#             json_data = request.get_json()
            
#             # req_fields = ['name', "handle", "bio", "profile_image"]

#             # for field in req_fields:
#             #     if field not in json_data:
#             #         return {
#             #            'status': 'failed',
#             #            'data': None,
#             #            'message': field + ' is required'
#             #         }, 400
#             #     elif json_data[field] == '':
#             #         return {
#             #            'status': 'failed',
#             #            'data': None,
#             #            'message': field + ' cannot be empty'
#             #         }, 400
#             #     else:
#             #         pass


#             result = save_user_to_db(json_data)
#             return {
#                 'status': 'success',
#                 'data': result, 
#                 'message': 'Account Service Successful.'
#             }, 200

#         except Exception as e:
#             return {
#                 'status': 'failed',
#                 'data': None,
#                 'message': str(e)
#             }, 500



