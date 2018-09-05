from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

def create_table(table_name):
    try:
        existing_table = client.describe_table(TableName = table_name)
    except Exception as e:
        print(e.args)
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'date',
                    'KeyType': 'SORT' #Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        print("Table status:", table.table_status)