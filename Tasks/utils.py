from binance.client import Client
import pandas as pd


def build_price_dataframe(trading_pairs, binance_client):
    dataframes = []
    for pair in trading_pairs:
        klines = binance_client.get_historical_klines(
            pair, Client.KLINE_INTERVAL_4HOUR, "2020-01-01")
        data = pd.DataFrame(klines, columns=['timestamp', 'Open', 'High', 'Low', '{}_close'.format(
            pair), 'Volume', 'Close_time', 'Quote_volume', 'Trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('timestamp', inplace=True)
        dataframes.append(data['{}_close'.format(pair)])
    master_df = pd.concat(dataframes, axis=1, ignore_index=False)
    master_df = master_df.astype(float)
    return master_df
