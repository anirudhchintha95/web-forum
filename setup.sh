#!/bin/bash
if [ ! -f /usr/bin/mongod ]
  then
    # Mongo Installation
    sudo apt-get install gnupg
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
      sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
      --dearmor

    # Use the below command for Ubuntu 20.04 (Focal)

    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] \
      https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | \
      sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    # echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] \
    #     https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
    #     sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo systemctl start mongodb
else
  echo "mongo db already installed.  Skipping..."
fi


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
