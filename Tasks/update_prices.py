import json
import pandas as pd
from binance.client import Client
import boto3
from os import environ

def run_update(event, context):

    # Getting S3 Bucket File Location
    bucket_name = environ.get("BUCKET")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    # API_KEY , API_SECRET
    API_KEY = environ.get("API_KEY")
    API_SECRET = environ.get("API_SECRET")

    # Creating Dummy Data
    dummy_csv = pd.DataFrame([API_KEY,API_SECRET])
    file_name = "testing.csv"
    dummy_csv.to_csv("/tmp/"+file_name,index=False,compression="gzip")

    # Upload File to s3
    path_to_file = f"/tmp/{file_name}"
    bucket.upload_file(path_to_file,file_name)
    
    response = {
        "statusCode": 200,
        "body": "Successfully created file"
    }

    return response