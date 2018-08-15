#!/bin/bash

echo "Deployment Started!"

rsync -r -I --quiet $TRAVIS_BUILD_DIR ubuntu@ec2-52-206-3-72.compute-1.amazonaws.com:apps

ssh ubuntu@ec2-52-206-3-72.compute-1.amazonaws.com "cd apps/shortlk; sudo sh docker.sh"