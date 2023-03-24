import logging
import os

from fastapi import HTTPException, Security
from fastapi.security import OpenIdConnect
from keycloak import KeycloakOpenID, KeycloakError
from pydantic import Json

oidc = OpenIdConnect(
    openIdConnectUrl="https://test.openml.org/aiod-auth/realms/dev/.well-known/openid-configuration"
)

keycloak_openid = KeycloakOpenID(
    server_url="https://test.openml.org/aiod-auth/",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    realm_name="dev",
    verify=True,
)


async def get_current_user(token=Security(oidc)) -> Json:
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
            status_code=401,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
