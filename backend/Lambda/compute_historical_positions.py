import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from time import mktime
import boto3
from os import environ
from utils import clean_name, convert_to_datetime

def compute_position(event, context):
    
    # Load Price from s3 bucket
    bucket_name = environ.get("BUCKET")
    usdt_file_name = environ.get("USDT_PRICE_FILE_NAME")
    client = boto3.client("s3")
    file = client.get_object(Bucket=bucket_name, Key=usdt_file_name)
    price_df = pd.read_csv(file["Body"], compression='gzip')

    order_history = json.loads(event['body'])['data']
    order_df = pd.DataFrame(order_history)
    order_df = order_df.apply(pd.to_numeric, errors='ignore')
    order_df = order_df[order_df['executedQty'] > 0]
    order_df = order_df[['symbol','executedQty','side','updateTime','price']]
    order_df['updateTime'] = order_df['updateTime'].apply(convert_to_datetime)

    order_df['symbol'] = order_df['symbol'].apply(clean_name)
    order_df.reset_index(inplace=True,drop=True)
    order_df['symbol'] = order_df['symbol'] + "USDT_close"
    order_df['side'] = np.where(order_df['side']=="BUY",1,-1)

    order_df['executedQty'] = order_df['executedQty'] * order_df['side']
    
    price_df = price_df[list(order_df['symbol'].unique())+['timestamp']]
    price_df['timestamp'] = pd.to_datetime(price_df['timestamp'])
    price_df = price_df[price_df['timestamp'] >= order_df['updateTime'].min()-timedelta(hours=4)] # [Potential Bug]
    price_df.set_index('timestamp',inplace=True)

    pos_df = pd.DataFrame(columns=price_df.columns)
    for t in price_df.index:
        temp = order_df[order_df['updateTime'] < t]
        temp = temp.groupby('symbol').sum()['executedQty']
        pos_df = pos_df.append(temp)
    pos_df.index = price_df.index
    nav_df = price_df.multiply(pos_df,axis=0)
    nav_df.index = pd.to_datetime(nav_df.index,"%Y-%m-%d")
    nav_df.columns = [clean_name(n) for n in list(nav_df.columns)]
    nav_df = nav_df.fillna(0)
    nav_timeseries_data = []
    for t in nav_df.index:
        unix_secs = mktime(t.timetuple())
        for col in nav_df.columns:
            nav_timeseries_data.append([unix_secs,col,nav_df.loc[t,col]])

    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
            },
        "body": json.dumps({
            "data": nav_timeseries_data
        })
    }

    return response
