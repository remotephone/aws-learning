
# https://linuxacademy.com/howtoguides/posts/show/topic/20419-creating-a-cloudwatch-billing-alarm
# This is not done. 


import argparse
import datetime
import json
import sys
import logging as log

import boto3

# Parse arguments
parser = argparse.ArgumentParser(description='Create an IAM user.')
parser.add_argument('-a', '--alarmname', required=True, help='Name your billing alarm')
parser.add_argument('-c', '--costpermonth', required=True, help='Trigger alarm when charges meet this value in $USD')
parser.add_argument('-d', '--alarmdescription', required=True, help='Describe your alarm in "\'s')

args = parser.parse_args()

alarmname = args.alarmname
costpermonth = args.costpermonth
alarmdescription = args.alarmdescription


# I want to query available sns topics and provide them as a list to the user

def get_topics():
    gottopics = []
    snsclient = boto3.client('sns')
    snstopics = snsclient.list_topics()

    for topic in snstopics['Topics']:
        gottopics.append(topic)
    print(gottopics)
    itemcount = len(gottopics)
    print(itemcount)
    rangecount = range(1, itemcount)
    print(enumerate(rangecount))
    optionslist = dict(zip(enumerate(rangecount), snstopics['Topics']))
    print(optionslist)



def check_alarms():
    cwclient = boto3.client('cloudwatch')
    try:
        alarmsnow = cwclient.describe_alarms()
        for alarm in alarmsnow['MetricAlarms']['AlarmName']:
            print(alarm)
    except:
        log.error("That didnt work")






def create_alarm(alarmname, alarmdescription, snstopic, costpermonth):
    cwclient = boto3.client('cloudwatch')
    resp = cwclient.put_metric_alarm(
        AlarmName=alarmname,
        AlarmDescription=alarmdescription,
        ActionsEnabled=True,
        OKActions=[
            snstopic,
        ],
        AlarmActions=[
            snstopic,
        ],
        InsufficientDataActions=[
            snstopic,
        ],
        MetricName='EstimatedCharges',
        Namespace='AWS/Billing',
        Statistic='Maximum',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            },
        ],
        Period=21600,
        EvaluationPeriods=1,
        Threshold=float(costpermonth),
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='ignore',
    )

    return resp


get_topics()
check_alarms()

# snstopic = input("What's the full of ARN of the topic you want to alert to?\n> ")
# resp = create_alarm(alarmname, alarmdescription, snstopic, costpermonth)

# print(resp) 