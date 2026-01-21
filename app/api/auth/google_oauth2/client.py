from authlib.integrations.starlette_client import OAuth

from app.env_config import stg


oauth = OAuth()
oauth.register(
    name='google',
    client_id=stg.client_id,
    client_secret=stg.client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'
    }
)
