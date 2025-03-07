import boto3

client = boto3.client('quicksight', region_name='us-east-1')

account_id = "970547378939"  # Replace with your actual AWS Account ID

response = client.list_dashboards(AwsAccountId=account_id)

for dashboard in response['DashboardSummaryList']:
    print(f"Dashboard Name: {dashboard['Name']}, Dashboard ID: {dashboard['DashboardId']}")