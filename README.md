## 群晖nas自用：

本项目基于gshang2017的Docker-qBittorrent-Enhanced-Edition，稍作修改增加了权限管理，以便于使用自己的账户权限运行，自用。

[https://hub.docker.com/repository/docker/superng6/qbittorrentee](https://hub.docker.com/repository/docker/superng6/qbittorrentee)

### 感谢以下项目:

[https://github.com/gshang2017/docker](https://github.com/gshang2017/docker)
[https://github.com/qbittorrent/qBittorrent](https://github.com/qbittorrent/qBittorrent)   
[https://github.com/c0re100/qBittorrent-Enhanced-Edition](https://github.com/c0re100/qBittorrent-Enhanced-Edition)    
[https://github.com/ngosang/trackerslist]( https://github.com/ngosang/trackerslist)

### 版本：
  
|名称|版本|说明|
|:-|:-|:-|
|qBittorrent|qee_4.2.1.10|增强版 (amd64)|


### 注意：

1. qBittorrent-Enhanced-Edition 增强版 需下载对应版本ipfilter.dat放入qBittorrent配置文件夹才能屏蔽离线下载 [https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases](https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases)

### docker命令行设置：


1. 创建qbittorrent容器

````
docker create  \
    --name=qbittorrentee  \
    -e WEBUIPORT=8989  \
    -p 6881:6881  \
    -p 6881:6881/udp  \
    -p 8989:8989  \
    -v /配置文件位置:/config  \
    -v /下载位置:/Downloads  \
    --restart unless-stopped  \
    johngong/qbittorrent:latest
````

2. 运行

       docker start qbittorrentee

3. 停止

       docker stop qbittorrentee

4. 删除容器

       docker rm qbittorrentee

5. 删除镜像

       docker image rm superng6/qbittorrentee:latest

### docker-compose
````
version: "2"
services:
  aria2:
    image: superng6/qbittorrentee
    container_name: qbittorrentee
    environment:
      - PUID=1026
      - PGID=100
      - TZ=Asia/Shanghai
    volumes:
      - /path/to/appdata/config:/config
      - /path/to/downloads:/Downloads
    ports:
      - 6881:6881
      - 6881:6881/udp
      - 8989:8989
    restart: unless-stopped
````



### 变量:

|参数|说明|
|-|:-|
| `--name=qbittorrentee` |容器名|
| `-p 8989:8989` |web访问端口 [IP:8989](IP:8989);(默认用户名:admin;默认密码:adminadmin);此端口需与容器端口和环境变量保持一致，否则无法访问|
| `-p 6881:6881` |BT下载监听端口|
| `-p 6881:6881/udp` |BT下载DHT监听端口
| `-v /配置文件位置:/config` |qBittorrent配置文件位置|
| `-v /下载位置:/Downloads` |qBittorrent下载位置|
| `-e WEBUIPORT=8989` |web访问端口环境变量|
| `-e TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|

### 群晖docker设置：

1. 卷

|参数|说明|
|-|:-|
| `本地文件夹1:/Downloads` |qBittorrent下载位置|
| `本地文件夹2:/config` |qBittorrent配置文件位置|

2. 端口

|参数|说明|
|-|:-|
| `本地端口1:6881` |BT下载监听端口|
| `本地端口2:6881/udp` |BT下载DHT监听端口|
| `本地端口3:8989` |web访问端口 [IP:8989](IP:8989);(默认用户名:admin;默认密码:adminadmin);此端口需与容器端口和环境变量保持一致，否则无法访问|

3. 环境变量：

|参数|说明|
|-|:-|
| `TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|
| `WEBUIPORT=8989` |web访问端口环境变量|

### 搜索：

#### 开启：视图-搜索引擎:
##### 说明：

1. 自带 [http://plugins.qbittorrent.org/](http://plugins.qbittorrent.org/) 部分搜索插件
2. 全新安装默认只开启官方自带部分和一个中文搜索插件。其它可到 视图-搜索引擎-界面右侧搜索-搜索插件-启动栏(双击)开启
3. 一些搜索插件网站需过墙才能用
4. jackett搜索插件需配置jackett.json(位置config/qBittorrent/data/nova3/engines)，插件需配合jackett服务的api_key。可自行搭建docker版jackett(例如linuxserver/jackett)。

### 其它:

1. Trackers只有一个工作,新增的Trackers显示还未联系，需在qBittorrent.conf里[Preferences]下增加Advanced\AnnounceToAllTrackers=true。可以参照我这篇博客操作https://sleele.com/2019/05/25/qbittorrent添加trackers后显示未联系
![](https://github.com/SuperNG6/pic/blob/master/issues/Xnip2019-12-23_20-39-50.png)
