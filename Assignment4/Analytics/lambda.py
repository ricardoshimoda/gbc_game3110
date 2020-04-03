import json
import datetime 
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Analytics')
    # we'll start by saving entries
    if event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'GameName' in body and 'Username' in body and 'EventName' in body and 'EventData' in body:

                if not verify_user(body['Username']):
                    return error_object('User not found: ' + body['Username'])

                if not verify_game(body['GameName']):
                    return error_object('Game not found: ' + body['GameName'])

                if not verify_event(body['EventName']):
                    return error_object('Event not found: ' + body['EventName'])

                item = {
                    'EventDate': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                    'GameName':  body['GameName'],
                    'Username':  body['Username'],
                    'EventName': body['EventName'],
                    'EventData': body['EventData']
                }
                table.put_item(
                    Item = item
                )
                return {
                    'statusCode': 200,
                    'body': '{"result": "Event logged successfully"}'
                }
            else:
                return error_object('Bad Request - needs to send GameName, Username, EventName, and EventData in the request body')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request body')
    else:
        return error_object('Only GET and POST are supported')

def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }

def verify_user(user_id):
    user = dynamodb.Table('Players')
    resp_user = user.get_item(Key={'user_id':user_id})
    return 'Item' in resp_user

def verify_game(game_name):
    game = dynamodb.Table('RemoteSettings')
    resp_game = game.get_item(Key={'GameName':game_name})
    return 'Item' in resp_game

def verify_event(event_name):
    event = dynamodb.Table('Event')
    resp_event = event.get_item(Key={'Name':event_name})
    return 'Item' in resp_event
