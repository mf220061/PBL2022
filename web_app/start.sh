#!/bin/bash

# rm -r ./flask_app/instance

docker container rm $(docker container ls -a -f status=exited -q)
docker container rm -f pbl-flask_app
docker container rm -f pbl-web
docker container rm -f pbl-adminer
docker container rm -f pbl-db

docker image rm $(docker image ls -a -f dangling=true -q)
docker image rm web_app_flask_app

docker volume rm $(docker volume ls -f dangling=true -q)

docker compose up
