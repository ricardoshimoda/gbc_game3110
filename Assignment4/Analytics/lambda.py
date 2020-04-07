import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

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
    elif event['httpMethod'] == 'GET':
        #Now we are querying the database
        if event['queryStringParameters']:
            # now we have to build the conditions
            query_request = event['queryStringParameters']
            params = Attr('EventDate').gt('0')
            if 'GameName' in query_request and query_request['GameName'] :
                params = params & Attr('GameName').eq(query_request['GameName'])
            if 'Username' in query_request and query_request['Username'] :
                params = params & Attr('Username').eq(query_request['Username'])
            if 'DateTimeStart' in query_request and query_request['DateTimeStart'] :
                params = params & Attr('EventDate').gte(query_request['DateTimeStart'])
            if 'DateTimeEnd' in query_request and query_request['DateTimeEnd'] :
                params = params & Attr('EventDate').lte(query_request['DateTimeEnd'])
            return {
                'statusCode': 200,
                'body': json.dumps(table.scan(FilterExpression = params), cls = CustomJsonEncoder)
            }
        else:
            # Performs a simple table scan
            return {
                'statusCode': 200,
                'body': json.dumps(table.scan(), cls = CustomJsonEncoder)#'{"result": "Getting all events"}'
            }
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

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

"""
{
    'resource': '/AnalyticsFunc', 
    'path': '/AnalyticsFunc',
     'httpMethod': 'GET', 
     'headers': 
     {
         'Accept': '*/*', 
         'Accept-Encoding': 'gzip, deflate, br', 
         'Cache-Control': 'no-cache', 
         'Content-Type': 'text/plain', 
         'Host': 'zfum6anmbl.execute-api.us-east-1.amazonaws.com', 
         'Postman-Token': 'fc0a5d05-ea84-4013-b6e0-26c4bd8d3ea6', 
         'User-Agent': 'PostmanRuntime/7.24.0', 
         'X-Amzn-Trace-Id': 'Root=1-5e88981a-d576563b9526715dac987b31', 
         'X-Forwarded-For': '142.116.183.116', 
         'X-Forwarded-Port': '443', 
         'X-Forwarded-Proto': 'https'
    },
    'multiValueHeaders': 
    {
        'Accept': ['*/*'], 
        'Accept-Encoding': ['gzip, deflate, br'], 
        'Cache-Control': ['no-cache'], 
        'Content-Type': ['text/plain'], 
        'Host': ['zfum6anmbl.execute-api.us-east-1.amazonaws.com'],
        'Postman-Token': ['fc0a5d05-ea84-4013-b6e0-26c4bd8d3ea6'], 
        'User-Agent': ['PostmanRuntime/7.24.0'], 
        'X-Amzn-Trace-Id': ['Root=1-5e88981a-d576563b9526715dac987b31'], 
        'X-Forwarded-For': ['142.116.183.116'], 
        'X-Forwarded-Port': ['443'], 
        'X-Forwarded-Proto': ['https']
    }, 
    'queryStringParameters': 
    {
        'ThisIsParam1': 'Param1', 
        'ThisIsParam2': 'Param2'
    }, 
    'multiValueQueryStringParameters': 
    {
        'ThisIsParam1': ['Param1'], 
        'ThisIsParam2': ['Param2']
    }, 
    'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '1nlnlt', 'resourcePath': '/AnalyticsFunc', 'httpMethod': 'GET', 'extendedRequestId': 'Kdy0GHlMoAMFyfw=', 'requestTime': '04/Apr/2020:14:22:18 +0000', 'path': '/default/AnalyticsFunc', 'accountId': '094268863370', 'protocol': 'HTTP/1.1', 'stage': 'default', 'domainPrefix': 'zfum6anmbl', 'requestTimeEpoch': 1586010138176, 'requestId': '1a2d33bf-6805-45c4-a520-0338c1b2f4dc', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '142.116.183.116', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.24.0', 'user': None}, 'domainName': 'zfum6anmbl.execute-api.us-east-1.amazonaws.com', 'apiId': 'zfum6anmbl'}, 'body': '{\n}', 'isBase64Encoded': False}
"""