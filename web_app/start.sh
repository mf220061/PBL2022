#!/bin/bash

docker container rm $(docker container ls -a -f status=exited -q)
docker container rm -f pbl-app
docker container rm -f pbl-web
docker container rm -f pbl-adminer
docker container rm -f pbl-db
docker image rm $(docker image ls -a -f dangling=true -q)
docker image rm web_app_app

docker compose up
