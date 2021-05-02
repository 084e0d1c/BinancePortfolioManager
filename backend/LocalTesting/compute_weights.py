from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import pandas as pd

# To do : Filter away very small amounts

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/compute_weights',methods=['POST'])
def compute_weights():
    assets = request.get_json()['data']
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
    
    max_weight = df["Weight"].max()
    coin_with_max_weight = df[df["Weight"] == max_weight].index[0]
    portfolio_value = df['Value'].sum()
    return jsonify({
        "code":200,
        "data":df.to_dict(),
        "plotting_data":plotting_data,
        "max_weight": round(max_weight*100,2),
        "coin_with_max_weight": coin_with_max_weight,
        "portfolio_value":round(portfolio_value,2)
    }),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=environ.get('PROD_ENV') != False)