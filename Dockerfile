FROM lsiobase/alpine:3.13 as builder
LABEL maintainer="SuperNG6"

ARG QBITTORRENT_VER=4.2.5.16
WORKDIR /qbittorrent
RUN wget https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases/download/release-${QBITTORRENT_VER}/qbittorrent-nox_linux_x64_static_build

# docker qBittorrent-Enhanced-Edition v4.2.5.16
FROM lsiobase/alpine:3.13

# environment settings
ENV TZ=Asia/Shanghai
ENV WEBUIPORT=8080

# add local files and install qbitorrent
COPY root /
COPY --from=builder /qbittorrent/qbittorrent-nox_linux_x64_static_build /usr/local/bin/qbittorrent-nox

# install python3
RUN  apk add --no-cache python3 \
&&   rm -rf /var/cache/apk/*   \
&&   chmod a+x  /usr/local/bin/qbittorrent-nox  

# ports and volumes
VOLUME /downloads /config
EXPOSE 8080  6881  6881/udp
