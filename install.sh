#!/usr/bin/env bash

# Check CPU architecture
ARCH=$(uname -m)

echo -e "${INFO} Check CPU architecture ..."
if [[ ${ARCH} == "x86_64" ]]; then
    ARCH="qbittorrent-nox_x86_64-linux-musl_static"
elif [[ ${ARCH} == "aarch64" ]]; then
    ARCH="qbittorrent-nox_aarch64-linux-musl_static"
elif [[ ${ARCH} == "armv7l" ]]; then
    ARCH="qbittorrent-nox_arm-linux-musleabi_static"
else
    echo -e "${ERROR} This architecture is not supported."
    exit 1
fi

# Download files
echo "Downloading binary file: ${ARCH}"
TAG=$(cat /qbittorrent/ReleaseTag)
echo "qbittorrent version: ${TAG}"
wget -O ${PWD}/qbittorrentee.zip https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases/download/release-${TAG}/${ARCH}.zip

echo "Download binary file: ${ARCH} completed"

unzip qbittorrentee.zip
