#!/usr/bin/env bash

set -e

# Check CPU architecture
ARCH=$(uname -m)

echo -e "${INFO} Check CPU architecture ..."
if [[ ${ARCH} == "x86_64" ]]; then
    ARCH="qbittorrent-enhanced-nox_x86_64-linux-musl_static.zip"
elif [[ ${ARCH} == "armv7l" ]]; then
    ARCH="qbittorrent-enhanced-nox_armv7-linux-musleabihf_static.zip"
elif [[ ${ARCH} == "aarch64" ]]; then
    ARCH="qbittorrent-enhanced-nox_aarch64-linux-musl_static.zip"
else
    echo -e "${ERROR} This architecture is not supported."
    exit 1
fi

# Download files
TAG=${QBITTORRENT_VERSION:-$(cat /qbittorrent/ReleaseTag)}
URL="https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases/download/release-$TAG/$ARCH"

echo "Downloading $ARCH for qBittorrent Enhanced Edition $TAG"
if ! curl --fail --location --silent --show-error --output qbittorrentee.zip "$URL" || [[ ! -s qbittorrentee.zip ]]; then
    echo "Failed to download a non-empty archive for $TAG ($ARCH)" >&2
    exit 1
fi

unzip qbittorrentee.zip
if [[ ! -s qbittorrent-nox ]]; then
    echo "Archive $ARCH does not contain a non-empty qbittorrent-nox binary" >&2
    exit 1
fi
