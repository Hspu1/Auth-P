from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request

homepage_rout = APIRouter(tags=["frontend"])


@homepage_rout.get("/", response_class=HTMLResponse, status_code=200)
def html_landing(request: Request) -> HTMLResponse:
    user = request.session.get("user")

    if user:
        first_name = user.get("given_name", "User")
        content = f"""
            <div class="glow-text">Welcome, {first_name}</div>
            <a href="/logout" class="login-btn">Log out</a>
        """
    else:
        content = """
            <div class="glow-text">Auth-P</div>
            <a href="/login" class="login-btn">Log in via Google</a>
        """

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Auth-P</title>
        <style>
            body {{
                margin: 0; padding: 0; height: 100vh;
                display: flex; align-items: center; justify-content: center;
                background-color: #121212; font-family: sans-serif; overflow: hidden;
            }}
            .center-container {{ text-align: center; }}
            .glow-text {{
                font-size: 64px; font-weight: bold; color: #32d69f;
                text-shadow: 0 0 10px rgba(50, 214, 159, 0.5), 0 0 20px rgba(50, 214, 159, 0.3);
                margin-bottom: 50px;
            }}
            .login-btn {{
                background-color: rgba(0, 0, 0, 0.6); color: white;
                border: 1px solid rgba(255, 255, 255, 0.2); padding: 15px 40px;
                cursor: pointer; font-size: 20px; font-weight: bold;
                border-radius: 4px; text-decoration: none;
                transition: all 0.2s ease-in-out;
            }}
            .login-btn:hover {{
                background-color: #1a1a1a;
                border-color: rgba(255, 255, 255, 0.8);
                color: #32d69f;
            }}
        </style>
    </head>
    <body>
        <div class="center-container">
            {content}
        </div>
    </body>
    </html>
    """)


@homepage_rout.get("/logout")
def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/")
