from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse

from app.env_config import stg


google_oauth2_router = APIRouter(tags=["google_oauth2"], prefix="/auth/google")

oauth = OAuth()
oauth.register(
    name='google',
    client_id=stg.client_id,
    client_secret=stg.client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
)


@google_oauth2_router.get("/login")
async def auth_google_login(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_oauth2_router.get(path="/callback")
async def auth_google_callback(request: Request) -> RedirectResponse:
    if request.query_params.get("error"):
        request.session.clear()
        return RedirectResponse(url="/?msg=access_denied")

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if user_info:
            request.session['user'] = {
                "given_name": user_info.get("given_name"),
                "picture": user_info.get("picture"),
                "email": user_info.get("email")
            }
        return RedirectResponse(url='/')

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e.error}")


@google_oauth2_router.get("/logout")
def auth_google_logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/")
