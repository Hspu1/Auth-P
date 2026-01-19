from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
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
async def html_landing(request: Request):
    user = await get_user(request=request)
    msg = request.query_params.get("msg")

    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user, "msg": msg}
    )
