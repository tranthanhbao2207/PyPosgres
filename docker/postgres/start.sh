#!/usr/bin/env bash

s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s" #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path

CONTAINER_NAME='gc_postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='psql'
#stop any previous running container
docker rm -f $(docker ps -qa -f name="$CONTAINER_NAME") &>/dev/null #TODO how to silent this command while &>/dev/null not working ref. https://stackoverflow.com/a/18062871/248616

#run postgres
docker-compose -f "$SCRIPT_HOME/docker-compose.yml" up -d --force-recreate #ref. https://forums.docker.com/t/named-volume-with-postgresql-doesnt-keep-databases-data/7434/2

#aftermath note
echo "
#after container run, we can use 'psql' via
docker exec -it $CONTAINER_NAME psql -U $POSTGRES_USER

#or 1/2 open bash prompt first
docker exec -it $CONTAINER_NAME bash #ref. https://askubuntu.com/a/507009/22308
#2/2 run psql
psql -U $POSTGRES_USER
"
