#!/bin/bash

[[ "$2" == "--update-all" ]] && export UPDATE_ALL=true
if [ "$1" == "--prod" ] ; then
    export DATA_50WORDS="/srv/data"
    export REPOSITORY_50WORDS="/srv/production"
    export LOG="INFO"
    docker-compose up
elif [ "$1" == "--staging" ] ; then
    export DATA_50WORDS="/srv/data"
    export REPOSITORY_50WORDS="/srv/staging"
    export LOG="INFO"
    docker-compose up
elif [ "$1" == "--dev" ] ; then
    export DATA_50WORDS="./data"
    export REPOSITORY_50WORDS="./dist"
    export LOG="DEBUG"
    docker-compose up
else
    echo "Usage: $0 [ --prod | --staging | --dev ] [ --update-all ]"
fi



