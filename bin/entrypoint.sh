#!/bin/bash


if [ $NODE_TYPE == "server" ]; then
    
    flask db upgrade
    
    SSL_CERT_URL=`cat "${SSL_CERT_URL}"`
    SSL_KEY_URL=`cat "${SSL_KEY_URL}"`
    
    mkdir -p /etc/ssl/certs/
    
    wget -O /etc/ssl/certs/rinnegan-locust.crt $SSL_CERT_URL
    chmod 644 /etc/ssl/certs/rinnegan-locust.crt
    
    wget -O /etc/ssl/certs/rinnegan-locust.key $SSL_KEY_URL
    chmod 600 /etc/ssl/certs/rinnegan-locust.key
    
    if [ $FLASK_ENV != "development" ]; then
        echo "Running Flask single threaded worker"
        newrelic-admin run-program flask run --host "0.0.0.0" --port 5000 --cert /etc/ssl/certs/rinnegan-locust.crt --key /etc/ssl/certs/rinnegan-locust.key
    else
        echo "Running Flask single threaded worker"
        flask run --host "0.0.0.0" --port 5000 --cert /etc/ssl/certs/rinnegan-locust.crt --key /etc/ssl/certs/rinnegan-locust.key
    fi
else
    mkdir -p /usr/src/app/data/worker-data
    REDIS_URL=`cat "${REDIS_URL_FILE}"`
    REDIS_QUEUE=`cat "${REDIS_QUEUE_FILE}"`
    rq worker --url $REDIS_URL $REDIS_QUEUE
fi
