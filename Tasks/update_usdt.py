import pandas as pd
from binance.client import Client
import boto3
from os import environ
from utils import build_price_dataframe
import json
import gzip

def run_update(event, context):

    # Getting valid tickers from S3 Bucket
    bucket_name = environ.get("BUCKET")
    file_name = environ.get("COIN_FILE_NAMES")
    client = boto3.client("s3")
    bucket = boto3.resource('s3').Bucket(bucket_name)
    file = client.get_object(Bucket=bucket_name,Key=file_name)

    # Process the valid tickers
    df = pd.read_csv(file["Body"], compression='gzip')
    list_of_coins = df['symbol'].unique()
    usdt_pairs = [p for p in list_of_coins if 'USDT' in p]

    # API_KEY , API_SECRET
    API_KEY = environ.get("API_KEY")
    API_SECRET = environ.get("API_SECRET")

    # Creating Dummy Data
    binance_client = Client(api_key=API_KEY, api_secret=API_SECRET)
    price_df = build_price_dataframe(['BTCUSDT','ETHUSDT'],binance_client)

    file_name = "usdt_prices.csv"
    price_df.to_csv("/tmp/"+file_name,index=False,compression="gzip")

    # Upload File to s3
    path_to_file = f"/tmp/{file_name}"
    bucket.upload_file(path_to_file,file_name)
    
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "msg":"Successfully update USDT pair prices",
            "dev":usdt_pairs
            })
    }

    return response