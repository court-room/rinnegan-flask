#!/bin/bash


if [ $NODE_TYPE == "server" ]; then
    
    flask db upgrade
    
    if [ $FLASK_ENV != "development" ]; then
        # echo "Running Gunicorn with eventlet workers"
        # gunicorn --bind 0.0.0.0:5000 --worker-class eventlet manage:app
        echo "Running Flask single threaded worker"
        newrelic-admin run-program flask run --host "0.0.0.0" --port 5000
    else
        echo "Running Flask single threaded worker"
        # gunicorn --bind 0.0.0.0:5000 manage:app
        flask run --host "0.0.0.0" --port 5000
    fi
else
    mkdir -p /usr/src/app/data/worker-data
    REDIS_URL=`cat "${REDIS_URL_FILE}"`
    REDIS_QUEUE=`cat "${REDIS_QUEUE_FILE}"`
    rq worker --url $REDIS_URL $REDIS_QUEUE
fi
