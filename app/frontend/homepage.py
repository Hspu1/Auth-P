from starlette.responses import HTMLResponse
from fastapi import APIRouter, Request

homepage_router = APIRouter(tags=["frontend"])


@homepage_router.get("/", response_class=HTMLResponse, status_code=200)
async def html_landing(request: Request) -> HTMLResponse:
    # юзай джинджу - на сейве готовые, только fu/cu. делай нормально
    user = request.session.get("user")
    msg = request.query_params.get("msg")

    error_html = ""
    if msg == "access_denied":
        error_html = '<div class="error-msg">Access denied by user</div>'

    if user:
        full_name = user.get("name")
        content = f"""
            <div class="glow-text">Welcome, {full_name}</div>
            <a href="/auth/google/logout" class="login-btn">Log out</a>
        """
    else:
        content = """
            <div class="glow-text">Auth-P</div>
            <a href="/auth/google/login" class="login-btn">Log in via Google</a>
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
            .center-container {{ 
                text-align: center; 
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
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
            .error-msg {{
                color: #ff4c4c;
                background: rgba(255, 76, 76, 0.1);
                border: 1px solid #ff4c4c;
                padding: 10px 20px;
                border-radius: 4px;
                margin-bottom: 30px;
                font-size: 16px;
                font-weight: bold;
                animation: fade-in 0.3s ease-out;
            }}
            @keyframes fade-in {{
                from {{ opacity: 0; transform: translateY(-10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
    </head>
    <body>
        <div class="center-container">
            {error_html}
            {content}
        </div>
    </body>
    </html>
    """)
