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

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    realm_name=os.getenv("KEYCLOAK_REALM"),
    verify=True,
)

KEYCLOAK_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
)


async def get_current_user(token=Security(oidc)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = token.replace("Bearer ", "")
        token_info = keycloak_openid.decode_token(token, key=KEYCLOAK_PUBLIC_KEY)
        return token_info
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
