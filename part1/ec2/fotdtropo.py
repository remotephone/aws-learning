from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2
import troposphere.iam as iam
from awacs.aws import Allow, Statement, Principal, Policy
from awacs.sts import AssumeRole



template = Template()


template.add_mapping('RegionMap', {
    "us-east-1": {"AMI": "ami-759bc50a"}
})


motd_userdata = """#!/bin/bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install apache2
    sudo systemctl enable apache2
    sudo systemctl restart apache2
    aws s3 sync aws-learning-confs-q324t432/motd/ /var/www/html/
    """

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))


ec2_s3_motd_role = template.add_resource(iam.Role(
    "CFNRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", ["ec2.amazonaws.com"])
            )
        ]
    )
))

cfninstanceprofile = template.add_resource(iam.InstanceProfile(
    "CFNInstanceProfile",
    Roles=[Ref(ec2_s3_motd_role)]
))


ec2_instance = template.add_resource(ec2.Instance(
    "ec2instance", 
    InstanceType="t2.micro",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    IamInstanceProfile="ec2_s3_motd_role",
    SecurityGroups = ["ec2_security_group"],
    UserData=Base64(motd_userdata)
))

# Security group that's applied to the Mount Targets.
ec2_security_group = ec2.SecurityGroup(
    "SecurityGroup",
    SecurityGroupIngress=[ec2.SecurityGroupRule(
        IpProtocol="tcp",
        FromPort="22",
        ToPort="22",
        CidrIp="0.0.0.0/0",
    ),],
    GroupDescription="Allow SSH over TCP"
)


ec2_security_group_rule = ec2.SecurityGroupRule(
    IpProtocol='tcp',
    FromPort='22',
    ToPort='22',
    SourceSecurityGroupId=Ref(ec2_security_group)
)


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

print(template.to_yaml())
