#!/bin/bash


if [ $NODE_TYPE == "server" ]; then
    
    flask db upgrade
    
    if [ $FLASK_ENV != "development" ]; then
        echo "Running Gunicorn with eventlet workers"
        
        NEW_RELIC_LICENSE_KEY=`cat $NEW_RELIC_LICENSE_KEY_FILE`
        NEW_RELIC_APP_NAME=`cat $NEW_RELIC_APP_NAME_FILE`
        
        sed -i -e "s/LICENSE_KEY_PLACEHOLDER/${NEW_RELIC_LICENSE_KEY}/g" newrelic.ini
        sed -i -e "s/APP_NAME_PLACEHOLDER/${NEW_RELIC_APP_NAME}/g" newrelic.ini
        
        NEW_RELIC_CONFIG_FILE=newrelic.ini  newrelic-admin run-program
        gunicorn --config gunicorn.conf.py manage:app
    else
        echo "Running the single threaded flask server"
        flask run --host 0.0.0.0
    fi
else
    mkdir -p /usr/src/app/data/worker-data
    REDIS_URL=`cat $REDIS_URL_FILE`
    rq worker --url $REDIS_URL rinnegan
fi
