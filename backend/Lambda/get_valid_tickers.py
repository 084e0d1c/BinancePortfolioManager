from os import environ
import boto3
import json
import pandas as pd


def get_valid_tickers(event, context):

    # Get latest prices of each coin from s3 bucket
    bucket_name = environ.get("BUCKET")
    coin_file_names = environ.get("COIN_FILE_NAMES")
    client = boto3.client("s3")
    file = client.get_object(Bucket=bucket_name, Key=coin_file_names)
    coins_df = pd.read_csv(file["Body"], compression='gzip')
    coins_df.drop_duplicates(keep="first", inplace=True)
    pairs = list(coins_df.set_index('symbol').to_dict()['price'].keys())

    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(pairs)
    }

    return response
