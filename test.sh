#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

python3 -m venv venv
. venv/bin/activate

./run.sh &
PID=$! # record the PID

newman run tests/default/forum_multiple_posts.postman_collection.json -e tests/default/env.json # use the env file
newman run tests/default/forum_post_read_delete.postman_collection.json -n 50 # 50 iterations

newman run tests/web-forum-API-tests.postman_collection.json