#!/bin/bash

curl -s -X POST $(echo $cache_url) \
    -H "X-Auth-Email: $cache_email " \
    -H "X-Auth-Key: $cache_key" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}' > /dev/null

echo "Cache Cleared"

echo "Deployment Started!"

rsync -r -I --quiet $TRAVIS_BUILD_DIR ubuntu@ec2-54-85-21-196.compute-1.amazonaws.com:apps

ssh ubuntu@ec2-54-85-21-196.compute-1.amazonaws.com "cd apps/shortlk; sudo sh docker.sh"
