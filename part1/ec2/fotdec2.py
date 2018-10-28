import argparse
import boto3
import json
import os
import requests



def get_ec2_iamprof(session):
    iamclient = session.client('iam')
    ec2profiles = iamclient.list_instance_profiles()
    for ec2profile in ec2profiles['InstanceProfiles']:
        print(ec2profile['InstanceProfileName'])


# need to test if group exists and handle that correctly. 
def check_the_env(session, profile):

    # This is the name of the security group, statically assigned
    secgroup_name = 'test_groupwow'


    # Create session, get security groups
    ec2client = session.client('ec2', region_name='us-east-1')
    ec2resource = session.resource('ec2', region_name='us-east-1')    

    groups_now = ec2client.describe_security_groups()

    #get my current IP for SSH access
    r = requests.get('https://api.ipify.org/')
    myip = r.text.rstrip('\n') + '/32'

    for group_now in groups_now['SecurityGroups']:
        print(group_now['GroupName'])
        print('-------------------')

        if secgroup_name in group_now['GroupName']:
            secgroup = ec2client.describe_security_groups(GroupNames=[secgroup_name])
            print('Group {} exists, moving on...'.format(secgroup_name))
            break
        else:
            print('Group {} not found, allowing 22 to you and 80 to all...'.format(secgroup_name))
            secgroup = ec2resource.create_security_group(GroupName=secgroup_name, Description='fotd sec group')
            secgroup.authorize_ingress(
                CidrIp=myip,
                IpProtocol='tcp',
                FromPort=22,
                ToPort=22
            )   
            secgroup.authorize_ingress(
                CidrIp='0.0.0.0/0',
                IpProtocol='tcp',
                FromPort=80,
                ToPort=80
            )
    print('leaving check_env')
    return secgroup

def create_new_inst(session, sec_group):
    motd_userdata = """#!/bin/bash
apt update && apt upgrade -y
apt install apache2 awscli -y
systemctl enable apache2
aws s3 sync s3://aws-learning-confs-q324t432/motd/ /var/www/html/
systemctl restart apache2
"""
        
    ec2 = session.resource('ec2', region_name='us-east-1')
    print(sec_group)
    # sec_group = sec_group['SecurityGroups']['GroupId']

    sec_group = sec_group['SecurityGroups'][0]['GroupId']
    instance = ec2.create_instances(ImageId='ami-759bc50a', InstanceType="t2.micro", 
        MaxCount=1, MinCount=1, SecurityGroupIds=[sec_group], UserData=motd_userdata,
        IamInstanceProfile={'Name': 'ec2_s3_motd_role'}, KeyName='linuxmint')
    return instance



def main():
    parser = argparse.ArgumentParser(description='spin up an ec2 instance that runs a fortune of the day job.')
    parser.add_argument('-p', '--profile', required=True, help='profile name from aws creds')
    args = parser.parse_args()

    profile = args.profile 

    session = boto3.Session(profile_name=profile)


    sec_group = check_the_env(session, profile)

        
    instance = create_new_inst(session, sec_group)
    print(instance.id)
    json.dumps(instance)


if __name__ == "__main__":
    main()