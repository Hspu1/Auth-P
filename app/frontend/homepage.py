from starlette.responses import HTMLResponse
from fastapi import APIRouter

homepage_rout = APIRouter()


@homepage_rout.get("/", response_class=HTMLResponse)
def html_landing():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Auth-P</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #121212;
                font-family: sans-serif;
                overflow: hidden;
            }
            .center-container {
                text-align: center;
            }
            .glow-text {
                font-size: 64px;
                font-weight: bold;
                color: #32d69f;
                text-shadow: 
                    0 0 10px rgba(50, 214, 159, 0.5),
                    0 0 20px rgba(50, 214, 159, 0.3);
                margin-bottom: 50px;
            }
            .login-btn {
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 15px 40px;
                cursor: pointer;
                font-size: 20px;
                font-weight: bold;
                border-radius: 4px;
                text-decoration: none;
                /* Плавный переход для комфорта глаз */
                transition: all 0.2s ease-in-out;
            }
            .login-btn:hover {
                /* Окрашиваем в цвет фона */
                background-color: #1a1a1a;
                /* Делаем рамку чуть ярче, чтобы выделить кнопку */
                border-color: rgba(255, 255, 255, 0.8);
                /* Текст остается белым или становится бирюзовым в тон заголовку */
                color: #32d69f;
            }
        </style>
    </head>
    <body>
        <div class="center-container">
            <div class="glow-text">Auth-P</div>
            <a href="/login" class="login-btn">Log in via Google</a>
        </div>
    </body>
    </html>
    """
