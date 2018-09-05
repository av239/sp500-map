import json
import os

from boto3.dynamodb.conditions import Key

import requests
from stock import decimalencoder
from helpers import helper
from stock import load


def list(event, context):
    dynamodb = helper.get_dynamo(context)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    fe = Key('date').eq(load.date_key())
    result = table.scan(FilterExpression = fe)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder),
        "headers": {
            'Access-Control-Allow-Origin': '*'
        }
    }

    return response


def get_price_data(ticker):
    url = "https://api.iextrading.com/1.0/stock/" + ticker + "/quote"
    response = requests.get(url=url)
    responseString = response.content.decode('utf-8')
    try:
        responseObject = json.loads(responseString)
    except:
        return None
    return responseObject