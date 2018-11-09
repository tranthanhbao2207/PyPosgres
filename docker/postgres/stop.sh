#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s" #get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
docker-compose -f "$SCRIPT_HOME/docker-compose.yml" down

#TODO we have > Removing network dbpostgres_default; where is this network from?