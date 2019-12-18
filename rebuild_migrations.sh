#!/usr/bin/env bash

find . -path "**/migrations/*.py" -not -name "__init__.py" -delete
find . -path "**/migrations/*.pyc"  -delete
rm ./db/db.sqlite3

REDIS_HOST=localhost REDIS_PORT=6379 python3 manage.py makemigrations
REDIS_HOST=localhost REDIS_PORT=6379 python3 manage.py migrate
