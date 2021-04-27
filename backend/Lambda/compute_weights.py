import json
import pandas as pd

def compute_weights(event, context):

    assets = json.loads(event['body'])['data']
    df = pd.DataFrame(assets)
    df = df.apply(pd.to_numeric,errors='ignore')
    df['Value'] = df['Quantity'] * df['Price']
    df['Weight'] = df['Value'].div(df['Value'].sum())
    df.set_index('Coin',inplace=True)
    data_dict = df.to_dict()
    plotting_data = []
    for coin in data_dict['Weight']:
        plotting_data.append({
            'label':coin,
            'value':data_dict['Weight'][coin]
        })

    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
            },
        "body": json.dumps({
            "data": df.to_dict(),
            "plotting_data":plotting_data
        })
    }

    return response
