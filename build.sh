#!/bin/bash

docker build \
    --build-arg HTTP_PROXY=http://172.17.0.1:7890 \
    --build-arg HTTPS_PROXY=http://172.17.0.1:7890 \
    --build-arg NO_PROXY=localhost,127.0.0.1 \
    --tag superng6/qbittorrentee:latest \
    --force-rm \
    .
