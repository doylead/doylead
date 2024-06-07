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
