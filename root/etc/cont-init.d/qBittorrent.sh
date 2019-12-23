#! /usr/bin/with-contenv bash

#检查config配置文件，并创建.
if [ ! -e "/config/qBittorrent/config/qBittorrent.conf" ] ;  then 
mkdir -p /config/qBittorrent/config/
cp /usr/local/qbittorrent/defaults/qBittorrent.conf  /config/qBittorrent/config/qBittorrent.conf
fi

#检查Search文件，并创建.
if [ ! -d "/config/qBittorrent/data/nova3/engines" ] ;  then 
mkdir -p /config/qBittorrent/data/nova3/engines
fi
cp -ru /usr/local/qbittorrent/defaults/Search/*  /config/qBittorrent/data/nova3/engines


#设定trackers更新任务
if [ `grep  -c updatetrackers.sh /var/spool/cron/crontabs/root` -eq 0 ];then
echo "0       0       *       *       *       /usr/local/qbittorrent/updatetrackers.sh" >> /var/spool/cron/crontabs/root
echo trackers更新任务已设定。
else
echo trackers更新任务已存在。
fi

chown -R abc:abc \
    /root \
    /usr \
	/config \
    /Downloads

#启动时更新trackers。
if [ "$TRACKERSAUTO" == "YES" ];then
/usr/local/qbittorrent/updatetrackers.sh
fi

#设置时区
ln -sf /usr/share/zoneinfo/$TZ   /etc/localtime 
echo $TZ > /etc/timezone
