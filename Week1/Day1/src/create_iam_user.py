import boto3

# Initialize IAM client
iam = boto3.client("iam")

# Define user name
user_name = "datalake_developer_2"

try:
    # Create IAM user
    response = iam.create_user(UserName=user_name)
    
    print(f"User {user_name} created successfully!")
    print(response)
    
except Exception as e:
    print(f"Error creating user: {str(e)}")


# Define policy ARN (AdministratorAccess or ReadOnlyAccess)
policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"

try:
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    print(f"Policy {policy_arn} attached to {user_name} successfully!")
except Exception as e:
    print(f"Error attaching policy: {str(e)}")

try:
    access_key_response = iam.create_access_key(UserName=user_name)
    print("Access Key Created Successfully!")
    print(access_key_response["AccessKey"])
except Exception as e:
    print(f"Error creating access key: {str(e)}")
try:
    iam.create_login_profile(
        UserName=user_name,
        Password="xxx",
        PasswordResetRequired=True
    )
    print(f"Login profile created for {user_name}. User must reset password on first login.")
except Exception as e:
    print(f"Error creating login profile: {str(e)}")
try:
    users = iam.list_users()
    for user in users["Users"]:
        print(f"User: {user['UserName']}, Created: {user['CreateDate']}")
except Exception as e:
    print(f"Error listing users: {str(e)}")
