#!/bin/bash

docker container rm $(docker conatiner ls -a -q)
docker image rm $(docker image ls -a -q)

docker compose up
