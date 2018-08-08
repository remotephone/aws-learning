import os

import boto3


def lambda_handler(event, context):
    client = boto3.client('sns')
    snstopic = os.environ.get("SNSTOPIC")
    responses = []

    for record in event['Records']:
        objectkey = record['s3']['object']['key']
        bucket = record['s3']['bucket']['name']
        message = "Object {}/{} delivered".format(bucket, objectkey)
        response = client.publish(TopicArn=snstopic,Message=message)
        responses.append(response)
    return responses