"""Allows high-level functionality for a web application using FastAPI"""

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from app.routers import google_authentication
from app.config import APP_SECRET_KEY, CONTACT_EMAIL, CONTACT_NAME

# TODO: When ready to add tag information to document methods
# https://fastapi.tiangolo.com/tutorial/metadata/

APP_DESCRIPTION = """
Serves as an organizational tool for both public and private use.

## Target Functionality
* Allow "backlog" creation and management
* Provide space for a blog

## Technology Used
* FastAPI / Python
"""

# Application overhead
app = FastAPI(
    title = "doylead",
    version = "0.1",
    description = APP_DESCRIPTION,
    contact = {
        "name": CONTACT_NAME,
        "email": CONTACT_EMAIL
    },
    # Set documentation location
    docs_url = "/docs",
    # For unambiguous documentation location
    redoc_url = None
)

app.add_middleware(
    SessionMiddleware,
    secret_key = APP_SECRET_KEY
)

app.mount(
    "/static",
    StaticFiles(directory = "static"),
    name = "static"
)

templates = Jinja2Templates(
    directory = "templates"
)

@app.get("/")
async def root(request: Request):
    """Returns root/index page, allows but does not require authentication"""
    print(APP_SECRET_KEY)
    print(CONTACT_EMAIL)
    print(CONTACT_NAME)
    return templates.TemplateResponse(
        name = "home.html",
        context = {"request": request}
    )

@app.get('/welcome')
def welcome(request: Request):
    """Returns a landing page after successful authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name = "welcome.html",
        context = {"request": request,
                   "user": user}
    )

# Add routes from other files
app.include_router(google_authentication.router)
