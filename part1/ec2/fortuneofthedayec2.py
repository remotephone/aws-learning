import boto3
import json
import os
import requests


ec2client = boto3.client('ec2')
ec2 = boto3.resource('ec2', region_name='us-east-1')
instance = ec2.Instance('id')

def get_my_ip():
    r = requests.get('https://api.ipify.org/')
    myip = r.text.rstrip('\n') + '/32'
    return myip

myip = get_my_ip()

secgroup_name = 'test_groupwow'

groups_now = ec2client.describe_security_groups()

motd_userdata = """#!/bin/bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install apache2
    sudo systemctl enable apache2
    sudo systemctl restart apache2
    aws s3 sync aws-learning-confs-q324t432/motd/ /var/www/html/
    """

def get_instance_profile():
    iamclient = boto3.client('iam')
    ec2profiles = iamclient.list_instance_profiles()
    for ec2profile in ec2profiles['InstanceProfiles']:
        print(ec2profile['InstanceProfileName'])



def create_new_inst():
    instance = ec2.create_instances(ImageId='ami-759bc50a', InstanceType="t2.micro", 
        MaxCount=1, MinCount=1, SecurityGroupIds=[sec_group.id], user_data=motd_userdata,
        IamInstanceProfile={'Name': 'ec2_s3_motd_role'})


# need to test if group exists and handle that correctly. 
def handle_sec_groups():
    for group_now in groups_now['SecurityGroups']:
        print(group_now['GroupName'])
        if secgroup_name in group_now['GroupName']:
            # create_new_inst()
            print('creating new instance')
        else:
            print('lol')
            sec_group = ec2.create_security_group(GroupName=secgroup_name, Description='slice_0 sec group')
            sec_group.authorize_ingress(
                CidrIp=myip,
                IpProtocol='tcp',
                FromPort=22,
                ToPort=22
            )   
            sec_group.authorize_ingress(
                CidrIp='0.0.0.0/0',
                IpProtocol='tcp',
                FromPort=80,
                ToPort=80
            )
            print('group made, creating instance')
            # create_new_inst()
            break

get_instance_profile()
handle_sec_groups()