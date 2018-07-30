import boto3
from argparse import ArgumentParser
from configparser import ConfigParser
import sys
import os 
from pathlib import Path, PurePath, PureWindowsPath

parser = ArgumentParser()
profile = parser.add_argument("-p", "--profile", help="Profile name, defaults to default", default="default")
duration = parser.add_argument("-d", "--duration", help="How long the token lasts, in hours - defaults to 4hrs/14400 seconds, max 36hrs", default="14400")
serial = parser.add_argument("-s", "--serial", help="SerialNumber for MFA token - ", default=None)
token = parser.add_argument("-t", "--token", help="MFA token from your app", required=True)
args = parser.parse_args()

profile = args.profile
duration = args.duration
token = args.token

try:
    if args.serial:
        serial = args.serial
    else:
        config = ConfigParser()
        awscreds = Path.home().joinpath('.aws', 'credentials')
        config.read(awscreds)
        serial = config.get(profile, 'mfa_serial')
        print(serial)
except:
    print('No MFA Serial Configured!')
    sys.exit(1)

session = boto3.session.Session(profile_name=profile)
client = session.client('sts')


try:
    response = client.get_session_token(
        DurationSeconds=int(duration),
        SerialNumber=serial,
        TokenCode=token
    )
    print(response['Credentials']['AccessKeyId'])
    print(response['Credentials']['SecretAccessKey'])
    print(response['Credentials']['SessionToken'])

except:
    print('oops')


