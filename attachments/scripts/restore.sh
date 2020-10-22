#!/bin/bash

# Example usage: ./scripts/restore.sh localhost 3309 root 123123
HOST=$1
PORT=$2
USER=$3
PASSWORD=$4

# Creating structure & Data
mysql -h ${HOST} --port ${PORT} -u ${USER} -p${PASSWORD} < attachments/mysql/dump.sql


