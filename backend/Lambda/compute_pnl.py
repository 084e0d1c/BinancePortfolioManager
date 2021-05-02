from os import environ
import pandas as pd
from datetime import datetime
from binance.client import Client
import boto3
import json
from utils import clean_name, convert_to_datetime


class CoinProfitLoss:

    def __init__(self,name):
        self.name = name
        self.cost_basis = 0
        self.realised_profit_loss = 0
        self.quantity = 0

    def buy(self,executedQty: float, price: float):
        self.quantity += executedQty
        self.cost_basis += executedQty * price

    def sell(self,executedQty: float, price: float):
        avg_purchase_price = self.cost_basis / self.quantity
        profit_loss = price - avg_purchase_price
        self.realised_profit_loss += profit_loss * executedQty
        self.quantity -= executedQty
        self.cost_basis = self.quantity * avg_purchase_price

    def get_realised_pnl(self):
        return self.realised_profit_loss

    def get_unrealised_pnl(self,current_price):
        current_mkt_value = self.quantity * current_price
        return current_mkt_value - self.cost_basis

    def total_pnl(self,current_price):
        return self.get_realised_pnl() + self.get_unrealised_pnl(current_price)

def get_reverse_trade_price(order,binance_client):
    order_time = int(order['updateTime'])
    start_date = str(convert_to_datetime(order_time).date())
    end_date = str(convert_to_datetime(order_time).date())
    # To patch this to take in price_df from s3 bucket or github repository
    moment_price_df = pd.DataFrame(binance_client.get_historical_klines("BTCUSDT",binance_client.KLINE_INTERVAL_30MINUTE,start_date,end_date)) # [Potential Bug]
    closest_price = moment_price_df[moment_price_df[0] < order_time].iloc[-1,4]
    return closest_price

def compute_pnl(event, context):
    
    json_payload = json.loads(event['body'])
    order_history = json_payload['order_history']
    binance_api_key = json_payload['API_KEY']
    binance_api_secret = json_payload['API_SECRET']

    binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

    # Get s3 bucket valid coins
    bucket_name = environ.get("BUCKET")
    coin_file_names = environ.get("COIN_FILE_NAMES")
    client = boto3.client("s3")
    file = client.get_object(Bucket=bucket_name, Key=coin_file_names)
    coins_df = pd.read_csv(file["Body"], compression='gzip')
    global price
    prices = coins_df.set_index('symbol').to_dict()['price']
    
    # Step 1: Get quantities of the coins
    valid_orders = [o for o in order_history if float(o['executedQty']) > 0]
    coin_obj_dict = {}
    pnl = {}
    for order in valid_orders:
        coin = order['symbol']
        if order['type'] == 'REVERSE':
            order['price'] = get_reverse_trade_price(order,binance_client)
        if coin not in coin_obj_dict:
            coin_obj_dict[coin] = CoinProfitLoss(coin)
        cpl_object = coin_obj_dict[coin]
        if order['side'] == 'BUY':
            cpl_object.buy(float(order['executedQty']),float(order['price']))
        else:
            cpl_object.sell(float(order['executedQty']),float(order['price']))
    category = []
    ureal_pnl = []
    real_pnl = []
    total_pnl_arr = []
    for coin in coin_obj_dict:
        # if coin_obj_dict[coin].cost_basis < 10:
        #     continue
        unrealised_pnl = coin_obj_dict[coin].get_unrealised_pnl(float(prices[coin]))
        realised_pnl = coin_obj_dict[coin].get_realised_pnl()
        category.append({
            "label":coin
        })
        ureal_pnl.append({
            "value":str(unrealised_pnl)
        })
        real_pnl.append({
            "value":str(realised_pnl)
        })
        total_pnl_arr.append(unrealised_pnl+realised_pnl)
    total_pnl = sum(total_pnl_arr)
    most_profitable = category[total_pnl_arr.index(max(total_pnl_arr))]["label"]
    least_profitable = category[total_pnl_arr.index(min(total_pnl_arr))]["label"]
    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
            },
        "body": json.dumps({
                "categories": category,
                "ureal_pnl":ureal_pnl,
                "real_pnl":real_pnl,
                "total_pnl":round(total_pnl,2),
                "most_profitable":most_profitable,
                "least_profitable":least_profitable
        })
    }

    return response
