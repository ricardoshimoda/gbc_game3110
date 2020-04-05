import json
import datetime 
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Players')
    # we'll start by saving entries
    if event['httpMethod'] == 'POST':
        if 'body' in event and event['body']:
            request_text = event['body']
            body = json.loads(request_text)
            if 'Password' in body and 'Username' in body :
                if not body['Username']:
                    return error_object('Bad Request - Username cannot be blank')
                if not body['Password']:
                    return error_object('Bad Request - Password cannot be blank')
                user_id = body['Username']
                try_pwd = body['Password']
                resp_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in resp_user:
                    item = resp_user['Item']
                    session_tk = str(uuid.uuid4())
                    if item['password'] == try_pwd:
                        table.update_item(
                            Key = {
                                'user_id' : user_id
                            },
                            UpdateExpression = 'SET session_tk = :val, login_date = :currentDate',
                            ExpressionAttributeValues={
                                ':val': session_tk,
                                ':currentDate':  datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                            }
                        )

                        return {
                            'statusCode': 200,
                            'body': '{"result": "User logged in successfully: (' + session_tk + ')"}'
                        }
                return error_object('Error - combination user/password not found')
            else:
                return error_object('Bad Request - needs to send Username and Password in the request body')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request body')
    else:
        return error_object('Only POST is supported')

def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }
