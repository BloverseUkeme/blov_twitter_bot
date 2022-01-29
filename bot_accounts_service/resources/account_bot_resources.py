# from flask_restful import Resource
# from flask import request
# # from bot_accounts_service.account_bot import save_handle_to_db
# # from bot_accounts_service.tasks.account import celery_account_save_to_db_from_bot


# class AccountBot(Resource):
#     def post(self):
#         try:
#             from bot_accounts_service.tasks.account import celery_account_save_to_db_from_bot
            
#             json_data = request.get_json()
            
#             req_fields = ["handle"]

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


#             json_data = json_data['handle']
#             result = celery_account_save_to_db_from_bot.apply_async((json_data,), queue="account")   
            
#             # result = save_handle_to_db(json_data)
#             return {
#                 'status': 'success',
#                 'data': None, 
#                 'message': 'Account Service Successful.'
#             }, 200

#         except Exception as e:
#             return {
#                 'status': 'failed',
#                 'data': None,
#                 'message': str(e)
#             }, 500



