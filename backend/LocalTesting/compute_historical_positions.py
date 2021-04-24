from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from time import mktime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def convert_to_datetime(t):
    dt = datetime.fromtimestamp(t/1000.0).strftime("%Y-%m-%d %H:%M:%S")
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

@app.route('/compute_historical_positions',methods=['POST'])
def compute_position():
    order_history = request.get_json()['data']
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
    price_df = pd.read_csv('../../DevFiles/Price.csv')
    price_df = price_df[list(order_df['symbol'].unique())+['timestamp']]
    price_df['timestamp'] = pd.to_datetime(price_df['timestamp'])
    price_df = price_df[price_df['timestamp'] >= order_df['updateTime'].min()-timedelta(hours=4)]
    price_df.set_index('timestamp',inplace=True)

    pos_df = pd.DataFrame(columns=price_df.columns)
    count = 0
    for t in price_df.index:
        count += 1
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
        unix_secs = int(mktime(t.timetuple()))
        for col in nav_df.columns:
            nav_timeseries_data.append([unix_secs,col,nav_df.loc[t,col]])

    return jsonify({
        'code':200,
        'data':nav_timeseries_data
    }),200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5003,debug=environ.get('PROD_ENV') != False)
