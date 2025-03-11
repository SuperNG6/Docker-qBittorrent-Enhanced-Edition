FROM superng6/alpine:3.21 AS builder
LABEL maintainer="SuperNG6"

WORKDIR /qbittorrent

COPY install.sh /qbittorrent/
COPY ReleaseTag /qbittorrent/

RUN apk add --no-cache ca-certificates curl jq

RUN cd /qbittorrent \
	&& chmod a+x install.sh \
	&& bash install.sh

# docker qBittorrent-Enhanced-Edition

FROM superng6/alpine:3.21

# environment settings
ENV TZ=Asia/Shanghai \
    WEBUIPORT=8080 \
    ENABLE_DOWNLOADS_PERM_FIX=true

# add local files and install qbitorrent
COPY root /
COPY --from=builder /qbittorrent/qbittorrent-nox /usr/local/bin/qbittorrent-nox

# install python3
RUN  apk add --no-cache python3 \
    && rm -rf /var/cache/apk/*  \
    && chmod a+x /usr/local/bin/qbittorrent-nox  

# ports and volumes
VOLUME /downloads /config
EXPOSE 8080 6881 6881/udp
