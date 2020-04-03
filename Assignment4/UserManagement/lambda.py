import json
import boto3

def lambda_handler(event, context):
    
    user_id = 'RicardoShimoda'
    print("this is where this all starts")
    print(event)
    print(context)
    if 'body' in event:
        request_text = event['body']
        body = json.loads(request_text)
        print(body)
        user_id = body['user_id']
    if 'user_id' in event:
        user_id = event['user_id']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Players')
    response = table.get_item(Key={'user_id':user_id})
    if 'Item' in response:
        table.update_item(
            Key = {
                'user_id' : body['user_id']
            },
            UpdateExpression = 'SET password = :pwd, email = :em',
            ExpressionAttributeValues={
                ':pwd': body['password'],
                ':em': body['email']
            }
        )
        item = response['Item']
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    else :
        # now we just have to learn how to write in a database
        table.put_item(
            Item = body
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('User Not Found')
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