#/bin/bash

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(dirname $SCRIPT_PATH)"
SRC_PATH="${APP_ROOT}/src"

cd $SRC_PATH

python main.py \
	--rebuild-db always \
	--fill-with-examples datasets publications news events case_studies presentations projects educational_resources \
	--url-prefix "" --reload