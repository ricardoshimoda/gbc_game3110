import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('BattleScore')
    #Now we are querying the database
    if event['queryStringParameters']:
        # now we have to build the conditions
        params = event['queryStringParameters']
        if 'user_id' in params and params['user_id']:
            user_id = params['user_id']
            if not verify_user(user_id):
                return error_object("user " + user_id + " not found on database")
            resp_score = table.get_item(Key={'user_id':user_id})
            if 'Item' in resp_score and resp_score['Item']:
                item = resp_score['Item']
                return {
                    'statusCode': 200,
                    'body': json.dumps(item,  cls = CustomJsonEncoder)
                }
            else:
                return error_object("Score not found for user " + user_id)
    return error_object("Need to send the following params through querystring: user_id, destroyed, kept, misses, rounds and they all must have a value - comeon!")

def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }

def verify_user(user_id):
    user = dynamodb.Table('Players')
    resp_user = user.get_item(Key={'user_id':user_id})
    return 'Item' in resp_user

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

"""
user_id: primary key - string 
destroyed: pieces destroyed in player's total career
kept: pieces kept at the end of the game in player's total career
misses: number of times the player has missed
rounds

"""