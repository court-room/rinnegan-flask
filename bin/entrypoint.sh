#!/bin/sh

if [ $STAGE != "local" ]; then
    flask db upgrade
fi

gunicorn --config /usr/src/app/gunicorn.conf.py manage:app
