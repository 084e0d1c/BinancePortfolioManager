from binance.client import Client
from flask import Flask, jsonify, request
from os import environ
from flask_cors import CORS
from time import sleep

# Round everything to 4 dp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def construct_pairs_prices(binance_client):

    all_tradable = binance_client.get_all_tickers()
    prices = {p['symbol']:p['price'] for p in all_tradable}
    all_pairs = [p['symbol'] for p in all_tradable if 'USDT' in p['symbol']]

    return all_pairs,prices

def clean_name(coin_name):
    CLEANING_SPLITS = ["USDT","BTC","BNB","ETH"]

    # Edge Cases
    if coin_name == "BTCUSDT" or coin_name == "BTCUSDT_close":
        return "BTC"
    if coin_name == "BNBUSDT" or coin_name == "BNBUSDT_close":
        return "BNB"
    if coin_name == "ETHUSDT" or coin_name == "ETHUSDT_close":
        return "ETH"

    clean_coin_name = coin_name
    for c in CLEANING_SPLITS:
        clean_coin_name = clean_coin_name.split(c)[0]
    return clean_coin_name

@app.route("/get_all_trades", methods=["POST"])
def get_all_trades():

    json_payload = request.get_json()
    binance_api_key = json_payload['API_KEY']
    binance_api_secret = json_payload['API_SECRET']
    additional_pairs = json_payload['EXTRA']

    binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

    all_pairs,prices = construct_pairs_prices(binance_client)
    
    all_pairs.extend(additional_pairs)
    # Step 1: Get quantities of the coins
    order_history = []
    reverse_order = [] # Suppose you trade DOTBNB , create a reverse order for BNB to "sell"
    qty_dict = {}
    qty_dict['BTC'] = 0
    for idx,pair in enumerate(all_pairs):
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
                    order_copy['executedQty'] = float(order_copy['price']) * float(order_copy['executedQty'])
                    order_copy['side'] = "SELL"
                    order_copy['type'] = "REVERSE" # This is for computing coin profit and loss
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
        assets[k] = [qty_dict[k],price_dict[k]]

    # Step 4: Get any USDT position 
    usdt_obj = binance_client.get_asset_balance("USDT")
    usdt_position = float(usdt_obj['free']) + float(usdt_obj['locked'])
    assets["USDT"] = [usdt_position,1]

    frontend_formatted_assets = []
    for coin in assets:
        temp = {}
        temp['Coin'] = coin
        temp['Quantity'] = assets[coin][0]
        temp['Price'] = assets[coin][1]
        temp['Value'] = float(temp['Price']) * float(temp['Quantity'])
        frontend_formatted_assets.append(temp)

    return jsonify(
        {
            "code":200,
            "data":{
                "assets":frontend_formatted_assets,
                "order_history":order_history,
            }
        }
    ),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=environ.get('PROD_ENV') != False)
