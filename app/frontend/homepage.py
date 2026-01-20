from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi_csrf_protect import CsrfProtect

from app.core.templates import templates

homepage_router = APIRouter(tags=["UI"])


async def get_user(request: Request) -> dict[str, str] | None:
    # wb redis huh
    user_id = request.session.get("user_id")
    user_name = request.session.get("full_name")

    if user_id and user_name:
        return {"name": user_name}
    return None


@homepage_router.get("/", response_class=HTMLResponse)
async def html_landing(request: Request, csrf_protect: CsrfProtect = Depends()):
    user = await get_user(request=request)
    msg = request.query_params.get("msg")
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    response = templates.TemplateResponse(
        "index.html", {
            "request": request,
            "user": user, "msg": msg,
            "csrf_token": csrf_token
        }
    )

    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
