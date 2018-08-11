import boto3


session = boto3.session.Session(profile_name='default-mfa', region_name='us-east-1')
cd = session.client('cur')



response = cd.put_report_definition(
    ReportDefinition={
        'ReportName': 'testreport',
        'TimeUnit': 'DAILY',
        'Format': 'textORcsv',
        'Compression': 'ZIP',
        'AdditionalSchemaElements': [
            'RESOURCES',
        ],
        'S3Prefix': 'reports',
        'S3Bucket': 'jaime-aws-billing-report',
        'S3Region': 'us-east-1'
    }
)

print(response)