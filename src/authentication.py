import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import OpenIdConnect
from keycloak import KeycloakOpenID, KeycloakError

load_dotenv()

oidc = OpenIdConnect(
    openIdConnectUrl=os.getenv("KEYCLOAK_OPENID_CONNECT_URL"),
    auto_error=False,
)

client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=client_secret,
    realm_name=os.getenv("KEYCLOAK_REALM"),
    verify=True,
)


async def get_current_user(token=Security(oidc)) -> dict:
    if not client_secret or " " in client_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="This instance is not configured correctly. You'll need to set the env var "
            "KEYCLOAK_CLIENT_SECRET (e.g. in src/.env). You need to obtain this secret "
            "from a Keycloak Administrator of AIoD.",
        )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = token.replace("Bearer ", "")
        return keycloak_openid.userinfo(token)
    except KeycloakError as e:
        logging.error(f"Error while checking the access token: '{e}'")
        error_msg = e.error_message
        if isinstance(error_msg, bytes):
            error_msg = error_msg.decode("utf-8")
        detail = "Invalid authentication token"
        if error_msg != "":
            detail += f": '{error_msg}'"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
