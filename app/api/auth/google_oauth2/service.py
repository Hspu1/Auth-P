from authlib.integrations.starlette_client import OAuthError
from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse

from app.api.auth.google_oauth2.client import oauth


async def callback_handling(request: Request) -> RedirectResponse:
    if request.query_params.get("error"):
        request.session.clear()
        return RedirectResponse(url="/?msg=access_denied")

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        print(user_info)
        if user_info:
            # передавай только id (UUID v7) из базы
            request.session['user'] = {
                "name": user_info.get("name"),
                "picture": user_info.get("picture"),
                "email": user_info.get("email"),
                "email_verified": user_info.get("email_verified"),
                "sub": user_info.get("sub"),
            }
        return RedirectResponse(url='/')

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e.error}")
