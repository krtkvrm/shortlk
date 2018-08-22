#!/bin/bash

curl -s -X POST $(echo $cache_url) \
    -H "X-Auth-Email: $cache_email " \
    -H "X-Auth-Key: $cache_key" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}' > /dev/null

echo "Cache Cleared"

echo "Frond End Deployment"

mkdir -p frontend/static

sed -i -e 's/shortlk/frontend/g' .bowerrc

bower install

sed -i -e 's/frontend/shortlk/g' .bowerrc

python3 shortlk/render.py > frontend/index.html

cp -R  shortlk/static frontend

./netlifyctl deploy -A $NETLIFY_KEY -s $NETLIFY_PROJECT_KEY -P frontend

echo "API Deployment Started!"

rsync -r -I --quiet $TRAVIS_BUILD_DIR ubuntu@ec2-52-206-3-72.compute-1.amazonaws.com:apps

ssh ubuntu@ec2-52-206-3-72.compute-1.amazonaws.com "cd apps/shortlk; sudo sh docker.sh"