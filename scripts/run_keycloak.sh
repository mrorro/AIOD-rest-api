#!/bin/bash

docker run \
	-p 8989:8989 \
	--name keycloak \
	--rm \
	--network sql-network \
	-e KEYCLOAK_ADMIN=admin \
	-e KEYCLOAK_ADMIN_PASSWORD=admin \
	aiod_keycloak:latest \
		start-dev \
		--db-username root \
		--db-password ok \
		--db-url-host sqlserver \
		--db-url-port 3306 \
		--db-url-database keycloak \
		--http-port 8989 \
		--db mysql
