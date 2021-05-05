from binance.client import Client
from time import sleep
from utils import clean_name
from os import environ
import boto3
import json
import pandas as pd


def get_all_trades(event, context):

    # Retrive traded pairs from events
    json_payload = json.loads(event['body'])['data']
    binance_api_key = json_payload['API_KEY']
    binance_api_secret = json_payload['API_SECRET']
    traded_pairs = json_payload['TRADED_PAIRS']

    binance_client = Client(api_key=binance_api_key,
                            api_secret=binance_api_secret)

    # Get latest prices of each coin from s3 bucket
    bucket_name = environ.get("BUCKET")
    coin_file_names = environ.get("COIN_FILE_NAMES")
    client = boto3.client("s3")
    file = client.get_object(Bucket=bucket_name, Key=coin_file_names)
    coins_df = pd.read_csv(file["Body"], compression='gzip')
    prices = coins_df.set_index('symbol').to_dict()['price']

    # Step 1: Get quantities of the coins
    order_history = []
    reverse_order = []  # Suppose you trade DOTBNB , create a reverse order for BNB to "sell"
    qty_dict = {}
    qty_dict['BTC'] = 0
    qty_dict['ETH'] = 0

    for idx, pair in enumerate(traded_pairs):
        if idx == 200:
            sleep(30)
        orders = binance_client.get_all_orders(symbol=pair)
        order_history.extend(orders)
        quantity = 0
        for order in orders:
            ex_qty = float(order['executedQty'])
            if order['side'] == 'BUY':
                quantity += ex_qty
            else:
                quantity -= ex_qty

            if ex_qty > 0:
                if pair.split('BTC')[-1] == "":
                    reverse_coin = 'BTC'
                elif pair.split('BNB')[-1] == "":
                    reverse_coin = 'BNB'
                elif pair.split('ETH')[-1] == "":
                    reverse_coin = 'ETH'
                else:
                    reverse_coin = False

                if reverse_coin:
                    order_copy = order.copy()
                    order_copy['time'] += 1
                    order_copy['updateTime'] += 1
                    order_copy['symbol'] = reverse_coin + "USDT"
                    order_copy['executedQty'] = float(
                        order_copy['price']) * float(order_copy['executedQty'])
                    order_copy['side'] = "SELL"
                    # This is for computing coin profit and loss
                    order_copy['type'] = "REVERSE"
                    reverse_order.append(order_copy)

        if orders:
            clean_coin_name = clean_name(pair)
            if clean_coin_name in qty_dict:
                qty_dict[clean_coin_name] += quantity
            else:
                qty_dict[clean_coin_name] = quantity

    # Step 1 Part 2: Resolve the reverse orders - this is very ugly code, but it works for now
    order_history.extend(reverse_order)
    for order in reverse_order:
        ex_qty = float(order['executedQty'])
        pair = order['symbol']
        clean_coin_name = clean_name(pair)

        if order['side'] == 'BUY':
            qty_dict[clean_coin_name] += ex_qty
        else:
            qty_dict[clean_coin_name] -= ex_qty

    # Step 2: Get current prices of coins in possession
    price_dict = {}
    for clean_coin_name in list(qty_dict.keys()):
        price_dict[clean_coin_name] = prices[clean_coin_name+"USDT"]

    # Step 3: Construct assets dictionary
    assets = {}
    for k in qty_dict:
        assets[k] = [qty_dict[k], price_dict[k]]

    # Step 4: Get any USDT position
    usdt_obj = binance_client.get_asset_balance("USDT")
    usdt_position = float(usdt_obj['free']) + float(usdt_obj['locked'])
    assets["USDT"] = [usdt_position, 1]

    frontend_formatted_assets = []
    for coin in assets:
        temp = {}
        temp['Coin'] = coin
        temp['Quantity'] = assets[coin][0]
        temp['Price'] = assets[coin][1]
        temp['Value'] = float(temp['Price']) * float(temp['Quantity'])
        if temp['Value'] > 1.0:
            frontend_formatted_assets.append(temp)

    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps({
            "assets": frontend_formatted_assets,
            "order_history": order_history,

        })
    }

    return response
