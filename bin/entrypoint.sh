#!/bin/bash


if [ $NODE_TYPE == "server" ]; then
    
    flask db upgrade
    
    if [ $FLASK_ENV != "development" ]; then
        echo "Running Gunicorn with eventlet workers"
        gunicorn --bind 0.0.0.0:5000 manage:app
    else
        echo "Running the single threaded flask server"
        flask run --host 0.0.0.0
    fi
else
    mkdir -p /usr/src/app/data/worker-data
    rq worker --url redis://:rinnegan@redis:6379/0 rinnegan
fi
