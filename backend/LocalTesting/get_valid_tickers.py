from binance.client import Client
from flask import Flask, jsonify, request
from os import environ
from flask_cors import CORS
from time import sleep
import pandas as pd

# Round everything to 4 dp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/get_tickers", methods=["GET"])
def get_valid_tickers():

    data = pd.read_csv('../../DevFiles/coins.csv',compression='gzip').drop_duplicates(keep='first').set_index('symbol').to_dict()
    pairs = list(data['price'].keys())
    return jsonify(
        {
            "code":200,
            "data": pairs
        }
    ),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5005,debug=environ.get('PROD_ENV') != False)
