import json
import pandas as pd

# Test Case: python-lambda-local -f compute_weights -t 5 handler.py test.json
# https://www.serverless.com/blog/serverless-python-packaging

def compute_weights(event, context):

    assets = event
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
        "statusCode": 200,
        "data": json.dumps(df.to_dict()),
        'headers': {'Content-Type': 'application/json'},
        "plotting_data":json.dumps(plotting_data)
    }

    return response
