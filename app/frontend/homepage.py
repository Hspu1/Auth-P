import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.templates import templates


homepage_router = APIRouter(tags=["UI"])


@homepage_router.get("/", response_class=HTMLResponse)
async def html_landing(request: Request):
    user = request.session.get("user")
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "msg": msg})


@homepage_router.get("/test-slow", response_class=HTMLResponse)
async def slow_data():
    await asyncio.sleep(2)
    return "<li>Новая задача из сервера</li>"
