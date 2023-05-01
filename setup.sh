#!/bin/bash
if [ ! -f /usr/bin/mongod ]
  then
    # Mongo Installation
    apt-get install gnupg

    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
    gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
    --dearmor

    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

    apt-get update
    apt-get install -y mongodb-org
    # start mongodb from the path
    /usr/bin/mongod --fork --logpath /var/log/mongodb/mongod.log --config /etc/mongod.conf
else
  echo "mongo db already installed.  Skipping..."
fi

echo "mongo db installed"

apt install python3.10-venv -y

python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
