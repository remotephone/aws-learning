import boto3
import json
import os
import requests


client = boto3.client('ec2')
ec2 = boto3.resource('ec2', region_name='us-east-1')
instance = ec2.Instance('id')


r = requests.get('http://www.myexternalip.com/raw')
myip = r.text.rstrip('\n') + '/32'
print(myip)

secgroup_name = 'test_groupwow'

groups_now = client.describe_security_groups()
# for group_now in groups_now['SecurityGroups'][group_now]['GroupName']:


def create_new_inst():
    instance = ec2.create_instances(ImageId='ami-759bc50a', InstanceType="t2.micro", 
        MaxCount=1, MinCount=1, SecurityGroupIds=[sec_group.id])




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
        print('done')
        break

