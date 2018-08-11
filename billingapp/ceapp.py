import argparse
import datetime
import json
import os
import csv

import boto3
import django

session = boto3.session.Session(profile_name='default-mfa')
cd = session.client('ce')



parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=30)
args = parser.parse_args()


now = datetime.datetime.utcnow()
start = (now - datetime.timedelta(days=args.days)).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')

results = []

token = None
while True:
    if token:
        kwargs = {'NextPageToken': token}
    else:
        kwargs = {}
    data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
    results += data['ResultsByTime']
    token = data.get('NextPageToken')
    if not token:
        break

print(json.dumps(results, indent=4))
# billing_parsed = {}
# for resultbytime in results[1]:
#     print(resultbytime)
#     billing_part = json.loads(resultbytime)
#     billing_parsed.update(billing_part)

# billing_data = open('/tmp/Billing.csv', 'w')

# csvwriter = csv.writer(billing_data)


# count = 0

# for bill in billing_parsed:
#     if count == 0:
#         header = bill.keys()
#         csvwriter.writerow(header)
#         count += 1
#     csvwriter.writerow(bill.values())

# billing_data.close()

# print('\t'.join(['TimePeriod', 'LinkedAccount', 'Service', 'Amount', 'Unit', 'Estimated']))
# for result_by_time in results:
#     for group in result_by_time['Groups']:
#         amount = group['Metrics']['UnblendedCost']['Amount']
#         unit = group['Metrics']['UnblendedCost']['Unit']
#         print(result_by_time['TimePeriod']['Start'], '\t', '\t'.join(group['Keys']), '\t', amount, '\t', unit, '\t', result_by_time['Estimated'])
