from datetime import datetime 
import pandas as pd

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

def convert_to_datetime(t):
    # Slightly different from backend, cos time is no longer in miliseconds once frontend converts it ~ 
    dt = datetime.fromtimestamp(t/1000).strftime("%Y-%m-%d %H:%M:%S")
    return pd.to_datetime(dt)