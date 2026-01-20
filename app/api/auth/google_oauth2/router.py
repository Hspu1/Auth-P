from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from fastapi_csrf_protect import CsrfProtect

from app.api.auth.google_oauth2.client import oauth
from app.api.auth.google_oauth2.service import callback_handling


google_oauth2_router = APIRouter(tags=["google_oauth2"], prefix="/auth/google")


@google_oauth2_router.get("/login")
async def login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_oauth2_router.get(path="/callback")
async def callback(request: Request) -> RedirectResponse:
    return await callback_handling(request=request)


@google_oauth2_router.post("/logout")
async def logout(request: Request, csrf_protect: CsrfProtect = Depends()) -> RedirectResponse:
    await csrf_protect.validate_csrf(request)

    request.session.clear()
    response = RedirectResponse(url="/", status_code=303)
    # 303 - переходим на ГЕТ при редиректе чтобы не дублировать ПОСТ
    # (могут быть неполадки с доп отправкой формы и тд)

    csrf_protect.unset_csrf_cookie(response)
    return response
