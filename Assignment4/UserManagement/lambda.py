import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Players')
    # we'll start by saving new entries
    if event['httpMethod'] == 'PUT':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'Username' in body and 'Email' in body and 'Password' in body and body['Username'] and body['Email'] and body['Password']:
                user_id = body['Username']
                resp_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in resp_user and resp_user['Item']:
                    return error_object('Error - user with username ' + body['Username'] + ' already exists - be creative - get another')
                new_entry = {
                    'user_id' : body['Username'],
                    'password': body['Password'],
                    'email': body['Email'],
                }
                table.put_item(
                    Item = new_entry
                )
                return {
                    'statusCode': 200,
                    'body': '{"result": "User registered successfully"}'
                }
            else:
                return error_object('Bad Request - needs to send Username, Email, and Password in the request body and they must not be empty')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request body')        
    elif event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'Username' in body and 'Email' in body and 'Password' in body and body['Username'] and body['Email'] and body['Password']:
                user_id = body['Username']
                resp_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in resp_user:
                    table.update_item(
                        Key = {
                            'user_id' : user_id
                        },
                        UpdateExpression = 'SET email = :email, password = :password',
                        ExpressionAttributeValues={
                            ':email': body['Email'],
                            ':password':  body['Password'],
                        }
                    )

                    return {
                        'statusCode': 200,
                        'body': '{"result": "User updated successfully"}'
                    }
                else:
                    return error_object('Error - user not found')
            else:
                return error_object('Bad Request - needs to send Username, Email, and Password in the request body')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request body')
    elif event['httpMethod'] == 'GET':
        #Now we are querying the database
        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if 'Username' in params and params['Username']:
                user_id = params['Username']
                resp_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in resp_user:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(resp_user['Item'], cls = CustomJsonEncoder)
                    }
                return error_object('Error - user not found')
            else:
                return error_object('Bad Request - needs to send Username in the request querystring')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request querystring with the Username')
    else:
        return error_object('Only GET, POST, and PUT are supported')

def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

