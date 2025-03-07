import boto3
import json

# AWS Configuration
AWS_REGION = "us-east-1"
USER_NAME = "data_admin_boto3"
INLINE_POLICY_NAME = "S3WriteOnlyPolicy"
MANAGED_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

# Initialize AWS clients
iam_client = boto3.client("iam", region_name=AWS_REGION)

# Inline policy document
inline_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}

# Create IAM user
def create_iam_user(user_name):
    try:
        response = iam_client.create_user(UserName=user_name)
        print(f"User '{user_name}' created successfully.")
        return response
    except iam_client.exceptions.EntityAlreadyExistsException:
        print(f"User '{user_name}' already exists.")
        return None

# Attach inline policy to IAM user
def attach_inline_policy(user_name, policy_name, policy_document):
    try:
        iam_client.put_user_policy(
            UserName=user_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        print(f"Inline policy '{policy_name}' attached to user '{user_name}' successfully.")
    except Exception as e:
        print(f"Error attaching inline policy: {e}")

# Attach managed policy to IAM user
def attach_managed_policy(user_name, policy_arn):
    try:
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        print(f"Managed policy '{policy_arn}' attached to user '{user_name}' successfully.")
    except Exception as e:
        print(f"Error attaching managed policy: {e}")

# Main function
def main():
    # Create IAM user
    create_iam_user(USER_NAME)

    # Attach inline policy
    attach_inline_policy(USER_NAME, INLINE_POLICY_NAME, inline_policy_document)

    # Attach managed policy
    attach_managed_policy(USER_NAME, MANAGED_POLICY_ARN)

if __name__ == "__main__":
    main()