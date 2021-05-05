import json
import pandas as pd


def compute_weights(event, context):

    assets = json.loads(event['body'])['data']
    df = pd.DataFrame(assets)
    df = df.apply(pd.to_numeric, errors='ignore')
    df['Value'] = df['Quantity'] * df['Price']
    df['Weight'] = df['Value'].div(df['Value'].sum())
    df.set_index('Coin', inplace=True)
    data_dict = df.to_dict()
    plotting_data = []
    for coin in data_dict['Weight']:
        plotting_data.append({
            'label': coin,
            'value': data_dict['Weight'][coin]
        })
    max_weight = df["Weight"].max()
    coin_with_max_weight = df[df["Weight"] == max_weight].index[0]
    portfolio_value = df['Value'].sum()
    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps({
            "data": df.to_dict(),
            "plotting_data": plotting_data,
            "max_weight": max_weight,
            "coin_with_max_weight": coin_with_max_weight,
            "portfolio_value": round(portfolio_value, 2)
        })
    }

    return response
