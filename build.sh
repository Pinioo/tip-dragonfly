#!/bin/bash

docker build -t dragonflydb -f Dockerfile.db ./
docker build -t bench -f Dockerfile.bench ./
