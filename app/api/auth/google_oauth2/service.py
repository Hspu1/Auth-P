from datetime import datetime, timezone

from authlib.integrations.starlette_client import OAuthError
from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse

from app.api.auth.google_oauth2.client import oauth
from app.core import UsersModel, UserIdentitiesModel
from app.core.db.database import async_session_maker


async def callback_handling(request: Request) -> RedirectResponse:
    if request.query_params.get("error"):
        request.session.clear()
        return RedirectResponse(url="/?msg=access_denied")

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if user_info:
            # передавай только id (UUID v7) из базы
            request.session[''] = {}
        return RedirectResponse(url='/')

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e.error}")


async def brainstorm_the_name_later(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    async with (async_session_maker() as session):
        async with session.begin():
            current_time, is_verified = (
                datetime.now(timezone.utc), user_info.get("email_verified", False)
            )

            new_user = UsersModel(
                email=user_info.get("email"), full_name=user_info.get("name"),
                email_verification_at=current_time if is_verified else None
            )
            new_user_identity = UserIdentitiesModel(
                provider="Google", provider_user_id=user_info.get("sub")
            )

            session.add(new_user, new_user_identity)
