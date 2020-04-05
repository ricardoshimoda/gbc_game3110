import json
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Score')
    # tries to find information about the game
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            print(params)
            if 'GameName' in params and 'Username' in params:
                score_key = params['Username'] + "|" + params['GameName']
                print(score_key)
                response = table.get_item(Key={'UserGame':score_key})
                if 'Item' in response:
                    item = response['Item']
                    return {
                        'statusCode': 200,
                        'body': json.dumps(item,  cls = CustomJsonEncoder)
                    }
                else :
                    return error_object('Score not found for this combination of Game / User')
            else:
                return error_object('Bad Request - needs to send GameName and Username in the request querystring parameter')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request querystring parameter')
    elif event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'GameName' in body and 'Username' in body and 'Score' in body:
                score_key = body['Username'] + '|' + body['GameName']
                response = table.get_item(Key={'UserGame':score_key})

                if not verify_user(body['Username']):
                    return error_object('User not found: ' + body['Username'])

                if not verify_game(body['GameName']):
                    return error_object('Game not found: ' + body['GameName'])

                if 'Item' in response:
                    table.update_item(
                        Key = {
                            'UserGame' : score_key
                        },
                        UpdateExpression = 'SET Score = :val',
                        ExpressionAttributeValues={
                            ':val': body['Score']
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': '{"result": Score updated successfully for user ' + body['Username'] + ' in game ' + body['GameName'] + ' "}'
                    }
                else :
                    #Creates a new entry
                    new_entry = {
                        'UserGame' : score_key,
                        'Score': body['Score']
                    }
                    table.put_item(
                        Item = new_entry
                    )
                    return {
                        'statusCode': 200,
                        'body': '{"result": Score created successfully for user ' + body['Username'] + ' in game ' + body['GameName'] + ' "}'
                    }
            else:
                return error_object('Bad Request - needs to send GameName, Username and Score in the request body')
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

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

