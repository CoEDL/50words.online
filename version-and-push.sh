#!/usr/bin/env bash
set -euo pipefail

if [ "$#" != "1" ] ; then
    echo "Usage: $0 [minor | patch]"
    exit 1
fi

if [[ $1 != 'minor'  && $1 != 'patch' ]] ; then
    echo "Usage: $0 [minor | patch]"
    exit 1
fi

# Bump the version, commit and tag atomically (npm version does all three).
npm version "$1"

# Push the commit and the new tag to trigger the container build.
git push origin master --follow-tags
