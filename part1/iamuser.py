##
# TODO: Add key creation
##
import argparse
import datetime
import json
import sys

import boto3

# Parse arguments
parser = argparse.ArgumentParser(description='Create an IAM user.')
parser.add_argument('-u', '--username', required=True, help='Username for new IAM User')
parser.add_argument('-p', '--path', required=False, help='Path for user. eg, Developers/tim', default='')
parser.add_argument('-k', '--key', required=False, help='set flag to create IAM key for user')
parser.add_argument('-d', '--delete', required=False, help='Delete user', action='store_true')
parser.add_argument('-c', '--create', required=False, help='Create user', action='store_true')
parser.add_argument('-p', '--policy', required=False, help='Create user', action='store_true')

args = parser.parse_args()

path = args.path
username = args.username
delete = args.delete
create = args.create

client = boto3.client('iam')

# Date time handler - json doesn't properly handle datetime objects
# https://stackoverflow.com/questions/35869985/datetime-datetime-is-not-json-serializable
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def deleter(username):
    check = input("Are you sure you want to delete user " + username + "?\nyes/no: ")
    if check.lower() == 'yes':
        iam = boto3.resource('iam')
        user = iam.User(username)
        response = user.delete()
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("User " + username + " deleted successfully")
        else:
            print('something went wrong')
    else:
        print("Thank you, exiting")
        sys.exit(1)

def creator(username, path):
    if path:
        response = client.create_user(Path=path, UserName=username)
        print(json.dumps(response, default=datetime_handler))
    else:
        response = client.create_user(UserName=username)
        print(json.dumps(response, default=datetime_handler))


if __name__ == '__main__':
    if delete:
        deleter(username)
    elif create:
        creator(username, path)
