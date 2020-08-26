#!/bin/sh

clear
sudo docker-compose build --compress --force-rm --parallel
sudo docker-compose up --detach --remove-orphans
