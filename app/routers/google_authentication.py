"""Allows oAuth/Google Authentication within the web application"""

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.config import CLIENT_ID, CLIENT_SECRET

# Allows us to route to endpoints in this file
router = APIRouter()

# It's not clear to me if we can avoid this duplication somehow
templates = Jinja2Templates(
    directory = "templates"
)

# Provides mechanism for oauth login, authentication, and logout
oauth = OAuth()
oauth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    client_kwargs = {
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

@router.get("/login")
async def login(request: Request):
    """Provides an endpoint for users to log in"""
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@router.get('/auth')
async def auth(request: Request):
    """Handles authentication with Google, saving user data in the session"""
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
        print(request.session['user'])
    return RedirectResponse('welcome')

@router.get('/logout')
def logout(request: Request):
    """Allows the user to logout, removing their data from the session"""
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')
