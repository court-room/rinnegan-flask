#!/bin/bash

flask db upgrade

if [ $NODE_TYPE == "server" ]; then
    if [ $FLASK_ENV != "development" ]; then
        echo "Running Gunicorn with eventlet workers"
        gunicorn --config /usr/src/app/gunicorn.conf.py manage:app
    else
        echo "Running the single threaded flask server"
        flask run --host 0.0.0.0
    fi
else
    celery worker -A app.celery --loglevel INFO
fi
