from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

from app.core.env_config import stg


class CsrfSettings(BaseModel):
    secret_key: str = stg.csrf_secret_key  # Берем из основного конфига
    cookie_samesite: str = "lax"  # allows cross-site request
    cookie_secure: bool = False  # True - https
    cookie_httponly: bool = True  # invisible cookie for JS (XSS protect)
    token_location: str = "body"
    token_key: str = "csrf-token"


@CsrfProtect.load_config
def get_csrf_config():
    print(f"DEBUG: CSRF Key loaded: {stg.csrf_secret_key}")  # Увидишь в консоли при запуске
    return CsrfSettings()
