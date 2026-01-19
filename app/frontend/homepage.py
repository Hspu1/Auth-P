from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core import UsersModel
from app.core.db.database import async_session_maker
from sqlalchemy import select
from app.core.templates import templates


homepage_router = APIRouter(tags=["UI"])


async def get_user(request: Request) -> dict[str, str]:
    user_id = request.session.get("user_id")
    if user_id:
        # wb redis instead pf pgsql (uuid) + refresh access idk
        async with async_session_maker() as session:
            stmt = select(UsersModel.full_name).where(UsersModel.id == user_id)
            full_name = (await session.execute(stmt)).scalar_one_or_none()
            if full_name:
                return {"name": full_name}


@homepage_router.get("/", response_class=HTMLResponse)
async def html_landing(request: Request):
    user = await get_user(request=request)
    msg = request.query_params.get("msg")

    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user, "msg": msg}
    )
