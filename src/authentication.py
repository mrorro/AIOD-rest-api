import logging
import os
import traceback

from fastapi import HTTPException, Security
from fastapi.security import OpenIdConnect
from keycloak import KeycloakOpenID
from pydantic import Json

oidc = OpenIdConnect(
    openIdConnectUrl="http://keycloak:8989/realms/dev/.well-known/openid-configuration"
)

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8989/",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    realm_name="dev",
    verify=True,
)


async def get_current_user(token=Security(oidc)) -> Json:
    try:
        token = token.replace("Bearer ", "")
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
