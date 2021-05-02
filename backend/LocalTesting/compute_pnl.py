from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import pandas as pd
from datetime import datetime
from binance.client import Client

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

def convert_to_datetime(t):
    # Slightly different from backend, cos time is no longer in miliseconds once frontend converts it ~ 
    dt = datetime.fromtimestamp(t/1000).strftime("%Y-%m-%d %H:%M:%S")
    return pd.to_datetime(dt)

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

def get_current_price(coin):
    return prices[coin]

def get_reverse_trade_price(order,binance_client):
    order_time = int(order['updateTime'])
    start_date = str(convert_to_datetime(order_time).date())
    end_date = str(convert_to_datetime(order_time).date())
    # To patch this to take in price_df from s3 bucket or github repository
    moment_price_df = pd.DataFrame(binance_client.get_historical_klines("BTCUSDT",binance_client.KLINE_INTERVAL_30MINUTE,start_date,end_date))
    closest_price = moment_price_df[moment_price_df[0] < order_time].iloc[-1,4]
    return closest_price

@app.route("/compute_pnl", methods=["POST"])
def compute_pnl():

    json_payload = request.get_json()
    binance_api_key = json_payload['API_KEY']
    binance_api_secret = json_payload['API_SECRET']
    order_history = json_payload['order_history']

    binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

    all_tradable = binance_client.get_all_tickers()
    global prices
    prices = {p['symbol']:p['price'] for p in all_tradable}
    
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
    for coin in coin_obj_dict:
        if coin_obj_dict[coin].cost_basis < 10:
            continue
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
    total_pnl = sum(ureal_pnl) + sum(real_pnl)
    total_pnl_arr = [ureal_pnl[i] + real_pnl[i] for i in range(len(ureal_pnl))]
    most_profitable = category[total_pnl_arr.index(max(total_pnl_arr))]
    least_profitable = category[total_pnl_arr.index(min(total_pnl_arr))]
    return jsonify(
        {
            "code":200,
            "data":{
                "categories": category,
                "ureal_pnl":ureal_pnl,
                "real_pnl":real_pnl,
                "total_pnl":total_pnl,
                "most_profitable":most_profitable,
                "least_profitable":least_profitable
            }
        }
    ),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5004,debug=environ.get('PROD_ENV') != False)
