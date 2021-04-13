FROM lsiobase/alpine:3.13 as builder
LABEL maintainer="SuperNG6"

ARG QBITTORRENT_VER=4.2.5.16
COPY install.sh /root/install.sh
RUN apk add --no-cache ca-certificates make g++ gcc qt5-qtsvg-dev boost-dev qt5-qttools-dev file
RUN chmod +x /root/install.sh && bash /root/install.sh

# docker qBittorrent-Enhanced-Edition v4.2.5.16
FROM lsiobase/alpine:3.13

# environment settings
ENV TZ=Asia/Shanghai
ENV WEBUIPORT=8080

# add local files and install qbitorrent
COPY root /
COPY --from=builder /qbittorrent /

# install python3
RUN  apk add --no-cache python3 \
&&   rm -rf /var/cache/apk/*   \
&&   chmod a+x  /usr/local/bin/qbittorrent-nox

# ports and volumes
VOLUME /downloads /config
EXPOSE 8080  6881  6881/udp
