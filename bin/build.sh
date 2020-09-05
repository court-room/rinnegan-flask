#!/bin/sh

clear
docker-compose build --compress --force-rm

docker image tag rinnegan-flask:latest localhost:6000/rinnegan-flask:latest

docker push localhost:6000/rinnegan-flask:latest