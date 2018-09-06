<!--
title: AWS Serverless REST API with DynamoDB store example in Python
description: This example demonstrates how visualize S&P 500 data using AWS Lambda, Dynamo DB, Python and Google Maps API. DynamoDB is used to store the data.
layout: Doc
-->
# Serverless API

This service demonstrates how to visualize where 500 most largest public companies in the US are located on the [Map](https://av239.github.io/Map.html). [DynamoDB](https://aws.amazon.com/dynamodb/) is used to store the data, [AWS Lambda](https://aws.amazon.com/lambda/) is the backend and Google Maps API to plot results. This is just an example and of course you could use any data storage as a backend.

## Structure

This service has a separate directory for all the operations required to download, parse and query stock data. It has 2 functions defined: `stock/list.py` which returns current snapshot of S&P 500 Companies and their market cap and `stock/load.py`. The load function parses a list of S&P 500 stock tickers and for each stock ticker get current market capitalization and location of company headquarters via Google Maps API.


## Setup

```bash
npm install
```

## Deploy

In order to deploy the endpoint simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service .zip file to S3 (1.59 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
....................
Serverless: Stack update finished...
Service Information
service: serverless-rest-api-with-dynamodb
stage: dev
region: us-west-1
stack: serverless-rest-api-with-dynamodb-dev
api keys:
  None
endpoints:
  GET - https://9dbbfoyqe1.execute-api.us-west-1.amazonaws.com/dev/stock
functions:
  list: serverless-rest-api-with-dynamodb-dev-list
  load: serverless-rest-api-with-dynamodb-dev-load
Serverless: Removing old service versions...
```

## Usage

You can create, retrieve, update, or delete todos with the following commands:

### List all tickers with coordinates

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/stock
```

Example output:
```bash
[{"createdAt": 1536202865815, "date": "2018-09-06", "id": "AMP", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [44.977753, -93.2650108]}, \"properties\": {\"mag\": 20417045580, \"companyName\": \"Ameriprise Financial Inc.\", \"address\": \"Minneapolis, MN, USA\"}}", "updatedAt": 1536202865815}, {"createdAt": 1536202953849, "date": "2018-09-06", "id": "ETR", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [29.95106579999999, -90.0715323]}, \"properties\": {\"mag\": 15365443519, \"companyName\": \"Entergy Corporation\", \"address\": \"New Orleans, LA, USA\"}}", "updatedAt": 1536202953849}, {"createdAt": 1536202842168, "date": "2018-09-06", "id": "ABBV", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [42.325578, -87.8411818]}, \"properties\": {\"mag\": 144143618123, \"companyName\": \"AbbVie Inc.\", \"address\": \"North Chicago, IL, USA\"}}", "updatedAt": 1536202842168}, {"createdAt": 1536203091021, "date": "2018-09-06", "id": "PFG", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [41.5868353, -93.6249593]}, \"properties\": {\"mag\": 15945930616, \"companyName\": \"Principal Financial Group Inc\", \"address\": \"Des Moines, IA, USA\"}}", "updatedAt": 1536203091021}, {"createdAt": 1536203072558, "date": "2018-09-06", "id": "NVDA", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [37.3541079, -121.9552356]}, \"properties\": {\"mag\": 169279360000, \"companyName\": \"NVIDIA Corporation\", \"address\": \"Santa Clara, CA, USA\"}}", "updatedAt": 1536203072558}, {"createdAt": 1536202972616, "date": "2018-09-06", "id": "FLR", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [32.8140177, -96.9488945]}, \"properties\": {\"mag\": 8004031829, \"companyName\": \"Fluor Corporation\", \"address\": \"Irving, TX, USA\"}}", "updatedAt": 1536202972616}, {"createdAt": 1536202978989, "date": "2018-09-06", "id": "IT", "feature": "{\"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": [41.0534302, -73.5387341]}, \"properties\": {\"mag\": 13939662648, \"companyName\": \"Gartner Inc.\", \"address\": \"Stamford, CT, USA\"}}", "updatedAt": 1536202978989}, {"createdAt": 1536203036807, "date": "2018-09-06", "id": "MRO", "feature": "{...]%
```

### Refresh all 500 tickers with current price info

```bash
# Replace the <id> part with a real id from your todos table
curl -X POST https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/stock/load<id>
```

No output

## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### DynamoDB

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```

In case you expect a lot of traffic fluctuation we recommend to checkout this guide on how to auto scale DynamoDB [https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/](https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/)
