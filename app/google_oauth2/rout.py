from os import getenv

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse

load_dotenv()
google_oauth2 = APIRouter(tags=["google_oauth2"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
)


@google_oauth2.get(path="/auth1")
async def auth1(request: Request) -> RedirectResponse:
    if request.query_params.get("error"):
        return RedirectResponse(url="/")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid auth token")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    request.session['user'] = dict(user_info)
    return RedirectResponse(url='/')


@google_oauth2.get(path="/login")
async def login(request: Request) -> RedirectResponse:
    redirect_uri = request.url_for('auth1')
    return await oauth.google.authorize_redirect(request, redirect_uri)
