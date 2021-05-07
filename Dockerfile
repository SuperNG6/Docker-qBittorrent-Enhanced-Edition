FROM lsiobase/ubuntu:focal as builder
LABEL maintainer="SuperNG6"

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /qbittorrent

RUN set -ex \
    && apt -y update \
    && DEBIAN_FRONTEND=noninteractive \
    && apt -y install build-essential pkg-config automake libtool git zlib1g-dev libssl-dev libgeoip-dev \
    libboost-dev libboost-system-dev libboost-chrono-dev libboost-random-dev \
    qtbase5-dev qttools5-dev libqt5svg5-dev

COPY ReleaseTag /qbittorrent/
COPY compile.sh /qbittorrent/

RUN set -ex \
    && chmod +x compile.sh && bash compile.sh

# docker qBittorrent
FROM lsiobase/ubuntu:focal

# add local files and install qbitorrent
COPY root /
COPY --from=builder /qbittorrent/qbittorrent /

# environment settings
ARG LD_LIBRARY_PATH=/usr/local/lib
ENV TZ=Asia/Shanghai \
    WEBUI_PORT=8080 \
    PUID=1026 PGID=100

# install python3
RUN apt -y update && DEBIAN_FRONTEND=noninteractive apt -y install python3 \
    && chmod a+x /usr/local/bin/qbittorrent-nox \
    && echo "**** cleanup ****" \
    && apt-get clean \
    && rm -rf \
       /tmp/* \
       /var/lib/apt/lists/* \
       /var/tmp/*

# ports and volumes
VOLUME /downloads /config
EXPOSE 8080  6881  6881/udp
