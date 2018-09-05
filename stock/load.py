import csv
import datetime
import decimal
import json
import os
import tempfile
import time

from botocore.exceptions import ClientError

import geojson
import requests
from stock.company import Company
from stock.googlemaps_api import get_coordinates
from stock import decimalencoder


#class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            if o % 1 > 0:
#                return float(o)
#            else:
#                return int(o)
#        return super(DecimalEncoder, self).default(o)


def get_feature(company):
    company_location = get_coordinates(company.companyName + " headquarters")
    try:
        my_point = geojson.Point((company_location.location["lat"], company_location.location["lng"]))
        my_feature = geojson.Feature(geometry=my_point,
                                     properties={"mag": company.marketCap,
                                                 "companyName": company.companyName,
                                                 "address": company_location.formatted_address})
        return my_feature
    except:
        return None


def load(event, context):
    result = get_sp500("https://datahub.io/core/s-and-p-500-companies/r/constituents.csv")

    from helpers.helper import get_dynamo
    dynamodb = get_dynamo(context)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    start_index = 0
    try:
        start_index = get_last_processed_ticker(result, table)
    except ClientError as e:
        print(e.response['Error']['Message'])
    except KeyError as e:
        print("Key Error")
    features = []
    processed = 0
    for ticker in result[start_index:]:
        try:
            processed += 1
            timestamp = int(time.time() * 1000)
            time_remaining = get_time_remaining(context)
            print("Time remaining (MS):", time_remaining)

            if ticker == result[-1]:
                print("Resetting last_processed ticker.")
                table.delete_item(
                    Key={
                        'id': "last_processed"
                    }
                )

            if time_remaining < 10 * 1000:  # 10 seconds
                save_processed_ticker(table, ticker, timestamp)
                break

            company = get_price_data(ticker)
            if company is None:
                print("Didn't get any info on:" + ticker)
                continue

            try:
                feature = get_feature(company)
            except:
                print("Unable to get feature for:" + ticker)
                continue
            if feature is None:
                continue
            features.append(feature)
            print("Processing company:" + company.companyName)

            item = {
                'id': ticker,
                'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                'feature': json.dumps(feature),
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }

            table.put_item(Item=item)
        except Exception as e:
            print(e.args)
            continue

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(features, cls=decimalencoder.DecimalEncoder)
    }

    return response


def save_processed_ticker(table, ticker, timestamp):
    item = {
        'id': "last_processed",
        'date': date_key(),
        'value': ticker,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    table.put_item(Item=item)
    print("last processed ticker saved: " + ticker)


def date_key():
    return datetime.datetime.today().strftime('%Y-%m-%d')


def get_last_processed_ticker(result, table):
    response = table.get_item(
        Key={
            'id': "last_processed",
            'date': datetime.datetime.today().strftime('%Y-%m-%d'),
        }
    )
    print(json.dumps(response, indent=4, cls=decimalencoder.DecimalEncoder))
    if isinstance(response['Item'], dict):
        for k, v in response.items():
            print(k, ' ', v)
    index = result.index(response['Item']['value'])
    if index >= 480:
        index = 0
    return index


def get_time_remaining(context):
    if context == None:
        # local execution
        return 1
    return context.get_remaining_time_in_millis()


def get_sp500(csvurl, print_output=False):
    r = requests.get(csvurl)
    f = tempfile.NamedTemporaryFile('wb')
    f.write(r.content)
    with open(f.name, 'rt', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        tickers = []
        for row in csvreader:
            if print_output:
                print(', '.join(row))
            if row[0] != 'Symbol':
                tickers.append(row[0])
    f.close()
    return tickers


def get_price_data(ticker):
    url = "https://api.iextrading.com/1.0/stock/" + ticker + "/quote"
    response = requests.get(url=url)
    responseString = response.content.decode('utf-8')
    try:
        responseObject = json.loads(responseString)
    except:
        return None

    return Company(marketCap=responseObject["marketCap"], symbol=responseObject["symbol"],
                   companyName=responseObject["companyName"])
