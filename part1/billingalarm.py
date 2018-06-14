
# https://linuxacademy.com/howtoguides/posts/show/topic/20419-creating-a-cloudwatch-billing-alarm
# This is not done. 


import argparse
import datetime
import json
import sys

import boto3

# Parse arguments
parser = argparse.ArgumentParser(description='Create an IAM user.')
parser.add_argument('-a', '--alarmname', required=True, help='Name your billing alarm')

args = parser.parse_args()

alarmname = args.alarmname
username = args.username
delete = args.delete
create = args.create


client = boto3.client('cloudwatch')

rresponse = client.put_metric_alarm(
    AlarmName='string',
    AlarmDescription='string',
    ActionsEnabled=True,
    OKActions=[
        'string',
    ],
    AlarmActions=[
        'string',
    ],
    InsufficientDataActions=[
        'string',
    ],
    MetricName='string',
    Namespace='string',
    Statistic='SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
    ExtendedStatistic='string',
    Dimensions=[
        {
            'Name': 'Currency',
            'Value': 'USD'
        },
    ],
    Period=21600,
    Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',
    EvaluationPeriods=123,
    DatapointsToAlarm=123,
    Threshold=123.0,
    ComparisonOperator='GreaterThanOrEqualToThreshold'|'GreaterThanThreshold'|'LessThanThreshold'|'LessThanOrEqualToThreshold',
    TreatMissingData='string',
    EvaluateLowSampleCountPercentile='string'
)