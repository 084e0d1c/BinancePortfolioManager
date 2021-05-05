import json
import boto3
from os import environ


def crud(event, context):

    # Load Dynamo Table
    table_name = environ.get('TABLE_NAME')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Get Payload
    json_payload = json.loads(event['body'])
    action = json_payload['action']
    uid = json_payload['uid']

    try:
        pairs = json_payload['pairs']
    except:
        pairs = ""

    if action == 'WRITE':
        item = {
            "uid": uid,
            "pairs": str(pairs)
        }
        table_resp = table.put_item(Item=item)
    else:
        table_resp = table.get_item(Key={'uid': uid})

    response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(table_resp)
    }

    return response
