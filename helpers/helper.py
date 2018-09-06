import boto3


def get_dynamo(context):
    if context == None:
        # local execution
        return boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    return boto3.resource('dynamodb')
