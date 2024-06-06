"""Allows access to protected variables"""

import os
from dotenv import load_dotenv

load_dotenv()

# Google OAuth
CLIENT_ID = os.environ.get('google-oauth-client-id', None)
CLIENT_SECRET = os.environ.get('google-oauth-client-secret', None)

# FastAPI Settings
APP_SECRET_KEY = os.environ.get('app-secret-key', None)
CONTACT_EMAIL = os.environ.get('contact-email', None)
CONTACT_NAME = os.environ.get('contact-name', None)

# AWS Settings
AWS_USER_KEY = os.environ.get('aws-user-key', None)
AWS_SECRET_KEY = os.environ.get('aws-secret-key', None)
AWS_RDS_SECRET_NAME = os.environ.get('aws-rds-secret-name', None)
AWS_RDS_ENDPOINT = os.environ.get('aws-rds-endpoint', None)
AWS_REGION = os.environ.get('aws-region', None)
