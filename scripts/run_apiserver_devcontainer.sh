#/bin/bash

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(dirname $SCRIPT_PATH)"
SRC_PATH="${APP_ROOT}/src"

cd $SRC_PATH

python main.py \
	--rebuild-db always \
	--populate-datasets example \
	--fill-with-examples publications news events case_study presentations \
	--url-prefix ""