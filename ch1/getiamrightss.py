## Expanding on the function here: https://gist.github.com/pandeybk/d643bef54007db831754

import boto3

iam = boto3.client('iam')
user = iam.list_users()
def find_user_and_groups():
    for userlist in user['Users']:
        userGroups = iam.list_groups_for_user(UserName=userlist['UserName'])
        userManagedPolicies = iam.list_attached_user_policies(UserName=userlist['UserName'])
        userPolicies = iam.list_user_policies(UserName=userlist['UserName'])
        print("Username: "  + userlist['UserName'])
        print("[-] Assigned groups: ")
        for groupName in userGroups['Groups']:
            print(groupName['GroupName'])
        print("[-] Directly attached policies: ")
        for policyName in userPolicies['PolicyNames']:
            print(policyName)
        print("[-] Attached managed policies: ")
        for policyName in userManagedPolicies['AttachedPolicies']:
            print(policyName['PolicyName'])
        print("----------------------------")

find_user_and_groups()