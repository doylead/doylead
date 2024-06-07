"""Provides basic connectivity to an AWS RDS resource"""

import os
from json import loads
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# AWS Config settings
AWS_USER_KEY = os.environ.get('aws-user-key', None)
AWS_SECRET_KEY = os.environ.get('aws-secret-key', None)
AWS_RDS_SECRET_NAME = os.environ.get('aws-rds-secret-name', None)
AWS_RDS_ENDPOINT = os.environ.get('aws-rds-endpoint', None)
AWS_REGION = os.environ.get('aws-region', None)

def get_secret(secret_name):
    """Retrieves secret key (rotated by AWS)"""

    # Creates an AWS session
    session = boto3.Session(
        aws_access_key_id = AWS_USER_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )

    # Create a Secrets Manager client
    client = session.client(
        service_name = 'secretsmanager',
        region_name = AWS_REGION
    )

    # Attempt to get RDS credentials.  If operations fail,
    # print error
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId = secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return loads(
        get_secret_value_response['SecretString']
    )

secret = get_secret(AWS_RDS_SECRET_NAME)
POSTGRES_DB = "postgres"
POSTGRES_USER = secret["username"]
POSTGRES_PASSWORD = secret["password"]
