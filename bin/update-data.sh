#!/bin/bash

[[ "$2" == "--update-all" ]] && export UPDATE_ALL=true
if [ "$1" == "--prod" ] ; then
    export DATA_50WORDS="/srv/data"
    export REPOSITORY_50WORDS="/srv/50words.online"
    export LOG="INFO"
    docker-compose up
elif [ "$1" == "--dev" ] ; then
    export DATA_50WORDS="./data"
    export REPOSITORY_50WORDS="./dist"
    export LOG="DEBUG"
    docker-compose up
else
    echo "Usage: $0 [ --prod | --dev ] [ --update-all ]"
fi



