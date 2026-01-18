from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from app.api.auth.google_oauth2.g_auth_config import oauth
from app.api.auth.google_oauth2.logic import g_auth_callback

google_oauth2_router = APIRouter(tags=["google_oauth2"], prefix="/auth/google")


@google_oauth2_router.get("/login")
async def auth_google_login(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_oauth2_router.get(path="/callback")
async def auth_google_callback(request: Request) -> RedirectResponse:
    return await g_auth_callback(request=request)


@google_oauth2_router.get("/logout")
def auth_google_logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/")
