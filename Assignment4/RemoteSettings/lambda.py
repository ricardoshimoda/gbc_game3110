import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RemoteSettings')
    # tries to find information about the game
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            if 'GameName' in params:
                game_name = params['GameName']
                response = table.get_item(Key={'GameName':game_name})
                if 'Item' in response:
                    item = response['Item']
                    return {
                        'statusCode': 200,
                        'body': json.dumps(item)
                    }
                else :
                    return error_object('Game not found: ' + game_name)
            else:
                return error_object('Bad Request - needs to send GameName in the request querystring parameter')
        else :
            # BAD Request
            return error_object('Bad Request - needs to send a request querystring parameter')
    elif event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'GameName' in body and 'Key' in body and 'Value' in body:
                game_name = body['GameName']
                response = table.get_item(Key={'GameName':game_name})
                if 'Item' in response:
                    game_var = body['Key']
                    game_val = body['Value']
                    table.update_item(
                        Key = {
                            'GameName' : game_name
                        },
                        UpdateExpression = 'SET ' + game_var + ' = :val',
                        ExpressionAttributeValues={
                            ':val': game_val
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': '{"result": "' + game_name + ' updated '  + game_var + ' successfully"}'
                    }
                else :
                    return error_object('Game not found: ' + game_name)
            else:
                return error_object('Bad Request - needs to send GameName, Key and Value in the request body')
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



"""
This is what event contains!!!!!!!
{
    'resource': '/MyFirstLambda', 
    'path': '/MyFirstLambda', 
    'httpMethod': 'POST', 
    'headers': 
    {   
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate, br', 
        'Cache-Control': 'no-cache', 
        'Content-Type': 'text/plain', 
        'Host': 'zfum6anmbl.execute-api.us-east-1.amazonaws.com', 
        'Postman-Token': '90f715c7-fe79-4e6a-a0e5-744758741099', 
        'User-Agent': 'PostmanRuntime/7.24.0', 
        'X-Amzn-Trace-Id': 'Root=1-5e85e3ef-39cc893e6fb8e17098e197c4', 
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
        'Postman-Token': ['90f715c7-fe79-4e6a-a0e5-744758741099'], 
        'User-Agent': ['PostmanRuntime/7.24.0'], 
        'X-Amzn-Trace-Id': ['Root=1-5e85e3ef-39cc893e6fb8e17098e197c4'], 
        'X-Forwarded-For': ['142.116.183.116'], 
        'X-Forwarded-Port': ['443'], 
        'X-Forwarded-Proto': ['https']}, 
        'queryStringParameters': None, 
        'multiValueQueryStringParameters': None, 
        'pathParameters': None, 
        'stageVariables': None, 
        'requestContext': 
        {
            'resourceId': '0lqgj2', 
            'resourcePath': '/MyFirstLambda', 
            'httpMethod': 'POST', 
            'extendedRequestId': 'KXCNbGdsIAMFnOg=', 
            'requestTime': '02/Apr/2020:13:09:03 +0000', 
            'path': '/default/MyFirstLambda', 
            'accountId': '094268863370', 
            'protocol': 'HTTP/1.1', 
            'stage': 'default', 
            'domainPrefix': 'zfum6anmbl', 
            'requestTimeEpoch': 1585832943402, 
            'requestId': '2b2a657b-4972-478a-877a-be5ff3035f88', 
            'identity': 
            {
                'cognitoIdentityPoolId': None, 
                'accountId': None, 
                'cognitoIdentityId': None, 
                'caller': None, 'sourceIp': 
                '142.116.183.116', 
                'principalOrgId': None, 
                'accessKey': None, 
                'cognitoAuthenticationType': None, 
                'cognitoAuthenticationProvider': None, 
                'userArn': None, 
                'userAgent': 'PostmanRuntime/7.24.0', 
                'user': None
            }, 
            'domainName': 'zfum6anmbl.execute-api.us-east-1.amazonaws.com', 
            'apiId': 'zfum6anmbl'
        }, 
        'body': '{"user_id":"Tesssst"}', 
        'isBase64Encoded': False
    }
"""