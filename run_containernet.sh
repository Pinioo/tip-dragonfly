#!/bin/bash

./build.sh
docker run --name containernet -it --rm --privileged --pid='host' -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/containernet/project containernet/containernet /bin/bash
