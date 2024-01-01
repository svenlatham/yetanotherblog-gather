#!/bin/bash

# Build the docker
docker build -t my-docker-image . || exit 1
docker run -v $(pwd)/output:/output my-docker-image || exit 1
