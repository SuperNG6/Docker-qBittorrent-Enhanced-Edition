#!/usr/bin/env bash

# Check CPU architecture
ARCH=$(uname -m)

echo -e "${INFO} Check CPU architecture ..."
if [[ ${ARCH} == "x86_64" ]]; then
    ARCH="x86_64"
elif [[ ${ARCH} == "aarch64" ]]; then
    ARCH="aarch64"
elif [[ ${ARCH} == "armv7l" ]]; then
    ARCH="armv7"
else
    echo -e "${ERROR} This architecture is not supported."
    exit 1
fi

#compiling qB

LIBTORRENT_VER=1.2.7
QBITTORRENT_VER=4.2.5.16

wget -P /qbtorrent https://github.com/arvidn/libtorrent/releases/download/libtorrent_`echo "$LIBTORRENT_VER"|sed 's#\.#_#g'`/libtorrent-rasterbar-${LIBTORRENT_VER}.tar.gz
tar  -zxvf  /qbtorrent/libtorrent-rasterbar-${LIBTORRENT_VER}.tar.gz   -C    /qbtorrent
cd  /qbtorrent/libtorrent-rasterbar-${LIBTORRENT_VER}
./configure  --host=${ARCH}-alpine-linux-musl
make install-strip
#qBittorrent-Enhanced-Edition
wget  -P /qbtorrent https://github.com/c0re100/qBittorrent-Enhanced-Edition/archive/release-${QBITTORRENT_VER}.zip
unzip   /qbtorrent/release-${QBITTORRENT_VER}.zip  -d    /qbtorrent
cd  /qbtorrent/qBittorrent-Enhanced-Edition-release-${QBITTORRENT_VER}
#
./configure   --disable-gui --host=${ARCH}-alpine-linux-musl
make install
ldd /usr/local/bin/qbittorrent-nox   |cut -d ">" -f 2|grep lib|cut -d "(" -f 1|xargs tar -chvf /qbtorrent/qbittorrent.tar
mkdir /qbittorrent
tar  -xvf /qbtorrent/qbittorrent.tar   -C  /qbittorrent
cp --parents /usr/local/bin/qbittorrent-nox  /qbittorrent
