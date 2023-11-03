#!/usr/bin/env bash

VERSION=$1
echo "Building $VERSION"

# build the 50words application container
npm run build:production
docker build --push --rm \
    -t ghcr.io/coedl/50words.online:latest .
