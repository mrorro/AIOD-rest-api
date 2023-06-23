#/bin/bash

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(dirname $SCRIPT_PATH)"
SRC_PATH="${APP_ROOT}/src"

docker run \
	--network sql-network\
	--rm \
	-p 8000:8000 \
	--name apiserver \
	-v $SRC_PATH:/app \
	ai4eu_server_demo \
	--rebuild-db always \
	--fill-with-examples datasets computational_resources publications news events case_studies \
	    presentations projects educational_resources organisations\
	--limit 10 \
	--url-prefix "" \
	--reload

