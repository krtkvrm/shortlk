#!/bin/bash

echo "Building Docker Image"

docker build -t  vkartik97/shortlk .

docker stop shortlk_w1

docker rm shortlk_w1

docker run -p 9091:8001 --name shortlk_w1 --env-file env.list -d vkartik97/shortlk

echo "First worker Deployed"

docker stop shortlk_w2

docker rm shortlk_w2

docker run -p 9092:8001 --name shortlk_w2 -d --env-file env.list vkartik97/shortlk

echo "Second Worker Deployed"

rm env.list