# from https://stackoverflow.com/a/32526487


import os
import argparse
import json
import sys
import boto3



# Parse arguments
parser = argparse.ArgumentParser(description='Quick and dirty copy one bucket to another.')
parser.add_argument('-s', '--source', required=True, help='source bucket')
parser.add_argument('-d', '--destination', required=True, help='destination bucket')

args = parser.parse_args()

source_bucket = args.source
dest_bucket = args.destination


if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'

from awscli.clidriver import create_clidriver
driver = create_clidriver()
driver.main('s3 mv s3://remotephone-dev-cloudtrail/log s3://aws-remotephone-cloudtrail-4ofj2jfgawser/test --recursive'.split())


# remotephone-dev-cloudtrail/logs aws-remotephone-cloudtrail-4ofj2jfgawser/test