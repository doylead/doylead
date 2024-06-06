"""Provides basic connectivity to an AWS RDS resource"""

import sys
from os import path
from json import loads
import psycopg2
import boto3
from botocore.exceptions import ClientError

# Allow us to import from .env
sys.path.append(
    path.join(path.dirname(__file__), '..')
)
from config import (AWS_USER_KEY, AWS_SECRET_KEY, 
    AWS_RDS_SECRET_NAME, AWS_RDS_ENDPOINT, AWS_REGION)

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

def postgres_db_connect(db_name = "doylead"):
    """Connects to Aurora Postgres instance"""
    # Get rotated passwords for RDS from AWS secret manager
    secret = get_secret(AWS_RDS_SECRET_NAME)

    # Attempt to connect to the database.  If operations fail,
    # print error
    try:
        conn = psycopg2.connect(host = AWS_RDS_ENDPOINT,
                                port = "5432",
                                database = db_name,
                                user = secret["username"],
                                password = secret["password"],
                                sslrootcert = "SSLCERTIFICATE")

    except Exception as e:
        print(f"Database connection failed due to {e}")

    return conn
