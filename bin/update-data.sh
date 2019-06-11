#!/bin/bash

if [ "$1" == "--prod" ] ; then
    export DATA_50WORDS="/srv/data"
    export REPOSITORY_50WORDS="/srv/50words.online"
    docker-compose up
elif [ "$1" == "--dev" ] ; then
    export DATA_50WORDS="./data"
    export REPOSITORY_50WORDS="./dist"
    docker-compose up
else
    echo "Usage: $0 [ --prod | --dev ]"
fi



