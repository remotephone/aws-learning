import boto3
from argparse import ArgumentParser
from configparser import ConfigParser
import sys
import os 
from pathlib import Path, PurePath

# parser = ArgumentParser()
# profile = parser.add_argument("-p", "--profile", help="Profile name, defaults to default", default="default")
# duration = parser.add_argument("-d", "--duration", help="How long the token lasts, in hours - defaults to 4hrs/14400 seconds, max 36hrs", default="14400")
# serial = parser.add_argument("-s", "--serial", help="SerialNumber for MFA token - ", default=None)
# token = parser.add_argument("-t", "--token", help="MFA token from your app", required=True)
# region = parser.add_argument("-r", "--region", help="Default region, defaults to us-east-1", default='us-east-1')
# args = parser.parse_args()


 
def get_serial(serial, awscreds, profile):
    try:
        config = ConfigParser()
        config.read(awscreds)
        serial = config.get(profile, 'mfa_serial')
        print(serial)
        return serial
    except:
        print('No MFA Serial Configured for ' + profile + ' profile!')
        sys.exit(1)


def get_token(profile, duration, serial, token):
    session = boto3.session.Session(profile_name=profile)
    client = session.client('sts')
    try:
        response = client.get_session_token(
            DurationSeconds=int(duration),
            SerialNumber=serial,
            TokenCode=token
        )
        acckey = response['Credentials']['AccessKeyId']
        seckey = response['Credentials']['SecretAccessKey']
        temptok = response['Credentials']['SessionToken']
        return acckey, seckey, temptok
    except:
        print('oops')


def update_creds(profile, awscreds, acckey, seckey, temptok):
    mfaprofname = profile + '-mfa'
    config = ConfigParser()
    config.read(awscreds)
    if config.has_section(mfaprofname) == True:
        config.set(mfaprofname, 'aws_access_key_id', acckey)
        config.set(mfaprofname, 'aws_secret_access_key', seckey)
        config.set(mfaprofname, 'aws_session_token', temptok)
        config.set()
    else:
        config.add_section(mfaprofname)
        config.set(mfaprofname, 'aws_access_key_id', acckey)
        config.set(mfaprofname, 'aws_secret_access_key', seckey)
        config.set(mfaprofname, 'aws_session_token', temptok)
    with open(awscreds, 'w') as configfile:
        config.write(configfile)

def update_config(profile, region):

    awsconfig = Path.home().joinpath('.aws', 'confog')
    config.read(awsconfig)
    if config.has_section(mfaprofname) == True:
        config.set(mfaprofname, 'default-region', region)
    else:
        config.add_section(mfaprofname)
        config.set(mfaprofname, 'default-region', region)



def main():
    parser = ArgumentParser()
    profile = parser.add_argument("-p", "--profile", help="Profile name, defaults to default", default="default")
    duration = parser.add_argument("-d", "--duration", help="How long the token lasts, in hours - defaults to 4hrs/14400 seconds, max 36hrs", default="14400")
    serial = parser.add_argument("-s", "--serial", help="SerialNumber for MFA token - ", default=None)
    token = parser.add_argument("-t", "--token", help="MFA token from your app", required=True)
    region = parser.add_argument("-r", "--region", help="Default region, defaults to us-east-1", default='us-east-1')
    args = parser.parse_args()

    profile = args.profile
    duration = args.duration
    token = args.token
    serial = args.serial
    config = ConfigParser()
    awscreds = Path.home().joinpath('.aws', 'credentials')
    config.read(awscreds)

    serial = get_serial(serial, awscreds, profile)
    print(serial)
    print(profile)
    acckey, seckey, temptok = get_token(profile, duration, serial, token)
    update_creds(profile, awscreds, acckey, seckey, temptok)
    update_config(profile, region)



if __name__ == "__main__":
    main()