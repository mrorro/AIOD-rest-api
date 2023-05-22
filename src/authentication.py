import logging
import os

from fastapi import HTTPException, Security, status
from fastapi.security import OpenIdConnect

from keycloak import KeycloakOpenID, KeycloakError


oidc = OpenIdConnect(
    openIdConnectUrl="https://test.openml.org/aiod-auth/realms/dev/.well-known/openid"
    "-configuration",
    auto_error=False,
)

keycloak_openid = KeycloakOpenID(
    server_url="https://test.openml.org/aiod-auth/",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    realm_name="dev",
    verify=True,
)

KEYCLOAK_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
)


async def get_current_user(token=Security(oidc)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in",
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
