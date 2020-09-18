#!/bin/bash


if [ $NODE_TYPE == "server" ]; then
    
    flask db upgrade
    
    if [ $FLASK_ENV != "development" ]; then
        echo "Running Gunicorn with eventlet workers"
        gunicorn --bind 0.0.0.0:5000 --worker-class eventlet manage:app
    else
        echo "Running Gunicorn with sync workers"
        gunicorn --bind 0.0.0.0:5000 manage:app
    fi
else
    mkdir -p /usr/src/app/data/worker-data
    rq worker --url redis://:rinnegan@redis:6379/0 rinnegan
fi
