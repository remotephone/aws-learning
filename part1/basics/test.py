import json
import boto3
from botocore.exceptions import ClientError
import argparse
import configparser

# POC to loop through profiles. Configure profiles in ~/.aws/config like this:
# [profile dev]
# role_arn = arn:aws:iam::123456789012:role/dev
# source_profile = master
#
# [profile qa]
# role_arn = arn:aws:iam::123456789012:role/qa
# source_profile = master
#
# ...etc...
# 
# Where "master" is an account that has rights to assume roles in each target account
#
# Sts class from https://blog.ashiny.cloud/2017/03/12/boto-sessions-and-aws-multi-account/

config = configparser.ConfigParser()


parser = argparse.ArgumentParser()
roles = parser.add_argument('-r', '--roles', action='append')
mfa = parser.add_argument('-m', '--mfa', required=False)
args = parser.parse_args()

if args.roles:
    roles = args.roles
else:
    roles = ['dev', 'qa', 'test']



class Sts(object):
    """
    Sts: Object to manage the persistence of authentication over multiple
        runs of an automation script. When testing a script this will
        save having to input an MFA token multiple times when using
        an account that requires it.
    """

    def __init__(self, role_arn, temporary_credentials_path, mfa_arn):
        self.temp_creds_path = temporary_credentials_path
        self.mfa_arn = mfa_arn
        self.role_arn = role_arn

    def get_temporary_session(self):
        """
        get_temporary_session: checks the temporary credentials stored
            on disk, if they fail to authenticate re-attempt to assume
            the role. The credentials requested last 15 minutes. For
            debugging purposes these can be persisted for up to an hour.
        """

        try:
            with open(self.temp_creds_path, 'r') as tmp_creds:
                credentials = json.loads(tmp_creds.read())
                client = boto3.client(
                    "sts",
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
                _ = client.get_caller_identity()["Account"]
        except (IOError, ClientError):
            response = boto3.client('sts').assume_role(
                DurationSeconds=900,
                RoleArn=self.role_arn,
                RoleSessionName='multi-account automation script',
                SerialNumber=self.mfa_arn,
                TokenCode=raw_input('MFA_Token:')
            )
            credentials = response['Credentials']
            with open(self.temp_creds_path, 'w') as tmp_creds:
                tmp_creds.write(json.dumps({
                    'AccessKeyId': credentials['AccessKeyId'],
                    'SecretAccessKey': credentials['SecretAccessKey'],
                    'SessionToken': credentials['SessionToken']}))

        return boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )

print(roles)
for role in roles:
    print(role)
    sesh = Sts(role_arn, temporary_credentials_path, mfa_arn)
    session = sesh.get_temporary_session()
    response = sts.assume_role()
    session = boto3.session.Session(profile_name=role)
    iam = session.client('iam')
    users = iam.list_users()
    for user in users['Users']:
        print(user['UserName'])



