#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

python3 -m venv venv
. venv/bin/activate

./run.sh &
PID=$! # record the PID

newman run tests/web-forum-API-tests.postman_collection.json