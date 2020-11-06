#!/bin/sh

# Set ARG
PLATFORM=$1
if [ -z "$PLATFORM" ]; then
    ARCH="64"
else
    case "$PLATFORM" in
        linux/amd64)
            ARCH="qbittorrent-nox_linux_x64_static.zip"
            ;;
        linux/arm/v7)
            ARCH="qbittorrent-nox_arm-linux-musleabi_static.zip"
            ;;
        linux/arm64|linux/arm64/v8)
            ARCH="qbittorrent-nox_aarch64-linux-musl_static.zip"
            ;;
        *)
            ARCH=""
            ;;
    esac
fi
[ -z "${ARCH}" ] && echo "Error: Not supported OS Architecture" && exit 1

# Download files
echo "Downloading binary file: ${ARCH}
TAG=cat /qbittorrent/ReleaseTag | head -n1
wget -O ${PWD}/qbittorrentee.zip https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases/download/release-${TAG}/${ARCH} /dev/null 2>&1


if [ $? -ne 0 ]; then
    echo "Error: Failed to download binary file: ${ARCH}" && exit 1
fi
echo "Download binary file: ${ARCH} completed"
unzip qbittorrentee.zip
