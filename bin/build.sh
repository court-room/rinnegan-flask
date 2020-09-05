#!/bin/sh

clear

docker build  --compress --force-rm --tag rinnegan-flask:latest .

docker image tag rinnegan-flask:latest localhost:6000/rinnegan-flask:latest

docker push localhost:6000/rinnegan-flask:latest
