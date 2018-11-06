
# https://linuxacademy.com/howtoguides/posts/show/topic/20419-creating-a-cloudwatch-billing-alarm
# This is not done. 


import argparse
import datetime
import json
import sys
import logging as log

from pick import pick
import boto3

# Parse arguments
parser = argparse.ArgumentParser(description='Create an IAM user.')
parser.add_argument('-a', '--alarmname', required=True, help='Name your billing alarm')
parser.add_argument('-c', '--costpermonth', required=True, help='Trigger alarm when charges meet this value in $USD')
parser.add_argument('-d', '--alarmdescription', required=True, help='Describe your alarm in "\'s')
parser.add_argument('-s', '--snstopic', required=False, help='Full ARN of SNS Topic to publish to')
parser.add_argument('-p', '--profile', required=True, help='profile name from aws creds')


args = parser.parse_args()

alarmname = args.alarmname
costpermonth = args.costpermonth
alarmdescription = args.alarmdescription
snstopic = args.snstopic
profile = args.profile
session = boto3.Session(profile_name=profile, region_name='us-east-1')

# I want to query available sns topics and provide them as a list to the user

def get_topics(session):
    snsclient = session.client('sns')
    snstopics = snsclient.list_topics()
    print("Which topic do you want to send notifications to?")

    # for topic in snstopics['Topics']:
    #     gottopics.append(topic)
    #     print("- " + topic['TopicArn'])

    options = snstopics['Topics']
    title = 'Pick an SNS topic to select'
    option = pick(options, title)
    print(options)
    gottopic = option[0]['TopicArn']

    return gottopic



def check_alarms(session, gottopic):
    cwclient = session.client('cloudwatch')
    alarms = []
    try:
        alarmsnow = cwclient.describe_alarms()
        for x in alarmsnow['MetricAlarms']:
            result = (x['AlarmName'])
            alarms.append(result)
    except:
        log.error("That didnt work")

    return alarms

def create_alarm(session, alarmname, alarmdescription, snstopic, costpermonth):
    cwclient = session.client('cloudwatch')
    resp = cwclient.put_metric_alarm(
        AlarmName=alarmname,
        AlarmDescription=alarmdescription,
        ActionsEnabled=True,
        OKActions=[
            snstopic
        ],
        AlarmActions=[
            snstopic
        ],
        InsufficientDataActions=[
            snstopic
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
    gottopic = snstopic
else:
    gottopic = get_topics(session)

print("now check_alarms")
alarmsnow = check_alarms(session, gottopic)
print(alarmsnow)
