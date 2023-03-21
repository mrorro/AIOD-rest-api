# AIoD + Authentication (Keycloak) demo

## Build and run the API, SQL and Keycloak

First of all, create a docker network:

```
docker network create sql-network
```

Then, open a terminal in the root folder to run the mysql server:

```bash
./scripts/run_mysql_server.sh
```

Open another terminal in the root folder to build and run the api:
```
docker build --tag ai4eu_server_demo:latest -f Dockerfile .
echo "# Authentication\nKEYCLOAK_CLIENT_ID=aiod-api\nKEYCLOAK_CLIENT_SECRET=ecA2lxThGQ+Apjdo7Wlv7yIi0H0D3ALof" > src/.env
./scripts/run_apiserver.sh
```

Open another terminal in the root folder to build and run keycloak
```
cd authentication
docker build --tag aiod_keycloak:latest -f Dockerfile . 
cd -
./scripts/run_keycloak.sh
```

## Setup keycloak
Open keycloak in your browser: http://localhost:8989.
Click on "master" (top left) and `CREATE REALM`. Then upload `authentication/realm-export.json`.

Now, we've got the problem that the dockerized API thinks that the keycloak is located at host 
`keycloak` (the name of the keycloak docker), while our keycloak console thinks that it's hosted at `localhost`. This is a problem for the authentication. The url of the keycloak is embedded in the token (the `iss` field), and must be the same as the url that the API uses, otherwise the API cannot authenticate the user. But... when accessing the Google Identity Provider, Google requires the redirect-url to be localhost.

This can be partially solved by:
- adding `127.0.0.1	keycloak` to `/etc/hosts`
- setting the `Frontend Url` of keycloak to `http://keycloak:8989` (you don't have to do this, 
  this is already in the realm)

Now, unfortunately, Google authentication does not work anymore using the API. But you can 
create a new user in keycloak, and authenticate with this!


## Usage
First, run the Mysql server, the Keycloak and the API (see above).

Then, use postman to setup authentication. See image:
![Postman Authentication](postman_authentication.png)

- As `auth url`, use http://keycloak:8989/realms/dev/protocol/openid-connect/auth
- As `Access token url`, use http://keycloak:8989/realms/dev/protocol/openid-connect/token
- As `client id`, use `aiod-api`
- As `client secret`, use `ecA2lxThGQApjdo7Wlv7yIi0H0D3ALof`

Then, you should be able to send a `GET` to `localhost:8000/authorization_test`, expecting a 
response like:

```json
{
    "msg": "success",
    "user": {
        "sub": "[uuid]",
        "email_verified": true,
        "name": "[Your name]",
        "preferred_username": "[Your username]",
        "given_name": "[First name]",
        "family_name": "[Last name]",
        "email": "[Email]"
    }
}
```