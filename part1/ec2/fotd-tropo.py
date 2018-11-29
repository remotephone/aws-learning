# Converted from EC2InstanceSample.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2
import yaml


with open('ec2s.yaml', 'r') as f:
    instances = yaml.load(f)

with open('secgroups.yaml', 'r') as f:
    secgroups = yaml.load(f)

template = Template()

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

template.add_mapping('RegionMap', {
    "us-east-1": {"AMI": "ami-0ac019f4fcb7cb7e6"},
    "us-east-2": {"AMI": "ami-0f65671a86f061fcd"},
    "us-west-1": {"AMI": "ami-063aa838bd7631e0b"}
})


secgroup1 = ec2.SecurityGroup(GroupName='security_group_1',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id
))

secgroup2 = ec2.SecurityGroup(GroupName='security_group_2',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id
))

template.add_resource(secgroup1)
template.add_resource(secgroup2)
    

tempalte.add_resource(ec2.VPC(CidrBlock='10.99.0.0/16',
                              AmazonProvidedIpv6CidrBlock=False,
                              InstanceTenancy='default'
))
out_net_learncf_1a.Value = Ref(net_learncf_1a)

template.add_resource(ec2.Subnet(AvailabilityZone='1a',
                                CidrBlock='10.99.10.0/24',
                                VpcId='string',
                                DryRun=True|False
)

response = client.create_vpc(
    CidrBlock='string',
    AmazonProvidedIpv6CidrBlock=True|False,
    DryRun=True|False,
    InstanceTenancy='default'|'dedicated'|'host'
)


ec2_instance = template.add_resource(ec2.Instance(
    "Ec2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=["default"],
    UserData=Base64("80"),
    
))

template.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(ec2_instance),
    ),
    Output(
        "AZ",
        Description="Availability Zone of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "AvailabilityZone"),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicDnsName"),
    ),
    Output(
        "PrivateDNS",
        Description="Private DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateDnsName"),
    ),
])

print(template.to_json())