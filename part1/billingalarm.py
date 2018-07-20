
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
parser.add_argument('-s', '--snstopic', required=False, help='Full ARN of SNS Topic to publish to')

args = parser.parse_args()

alarmname = args.alarmname
costpermonth = args.costpermonth
alarmdescription = args.alarmdescription
snstopic = args.snstopic

# I want to query available sns topics and provide them as a list to the user

def get_topics():
    gottopics = []
    snsclient = boto3.client('sns')
    snstopics = snsclient.list_topics()
    print("Which topic do you want to send notifications to?")

    for topic in snstopics['Topics']:
        gottopics.append(topic)
        print("- " + topic['TopicArn'])
    # itemcount = len(gottopics)
    # rangecount = range(0, itemcount)
    # optionslist = dict(zip(rangecount), snstopics['Topics'])
    # print(optionslist)
    # return optionslist
    return gottopics



def check_alarms(gottopics):
    cwclient = boto3.client('cloudwatch')
    try:
        alarmsnow = cwclient.describe_alarms()
        print(alarmsnow)
        for k, v  in alarmsnow['MetricAlarms']['AlarmName']:
            print(v)
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

if snstopic:
    gottopics = snstopic
else:
    gottopics = get_topics()

print("now check_alarms")
check_alarms(gottopics)
