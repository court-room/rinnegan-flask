#!/bin/sh

if [ $STAGE != "local" ]; then
    flask db upgrade
fi

# gunicorn --config /usr/src/app/gunicorn.conf.py manage:app
flask run -h 0.0.0.0
