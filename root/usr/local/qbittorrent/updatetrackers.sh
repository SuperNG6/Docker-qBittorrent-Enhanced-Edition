#! /bin/sh

if [ "$TRACKERSAUTO" == "YES" ];then

curl -so  /tmp/trackers_all.txt https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt
#wget -qP  /tmp  https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt --no-check-certificate 
Newtrackers="Bittorrent\TrackersList=$(awk '{if(!NF){next}}1'  /tmp/trackers_all.txt|sed ':a;N;s/\n/\\n/g;ta' )"
Oldtrackers="`grep  TrackersList=  /config/qBittorrent/config/qBittorrent.conf`" 
echo $Newtrackers >/tmp/Newtrackers.txt

if [  -e "/tmp/trackers_all.txt" ] ;  then 

if [ "$Newtrackers" == "$Oldtrackers" ];then
echo trackers文件一样,不需要更新。
else
sed  -i   '/Bittorrent\\TrackersList=/r /tmp/Newtrackers.txt'    /config/qBittorrent/config/qBittorrent.conf 
sed  -i   '1,/^Bittorrent\\TrackersList=.*/{//d;}'  /config/qBittorrent/config/qBittorrent.conf 
#kill qBittorrent
ps -ef |grep profile |grep -v grep|awk '{print $1}'|xargs kill -9
echo 已更新trackers。
fi

rm  /tmp/trackers_all.txt
rm  /tmp/Newtrackers.txt

else
echo 更新文件未正确下载，更新未成功，请检查网络。

fi

else

echo 未设定自动更新trackers。
fi



