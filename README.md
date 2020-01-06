## 群晖nas自用：

本项目基于gshang2017的Docker-qBittorrent-Enhanced-Edition，稍作修改增加了权限管理，以便于使用自己的账户权限运行，自用。

[https://hub.docker.com/r/superng6/qbittorrentee](https://hub.docker.com/r/superng6/qbittorrentee)

### 感谢以下项目:

[https://github.com/gshang2017/docker/tree/master/qBittorrent](https://github.com/gshang2017/docker/tree/master/qBittorrent)   
[https://github.com/qbittorrent/qBittorrent](https://github.com/qbittorrent/qBittorrent)   
[https://github.com/c0re100/qBittorrent-Enhanced-Edition](https://github.com/c0re100/qBittorrent-Enhanced-Edition)    
[https://github.com/ngosang/trackerslist]( https://github.com/ngosang/trackerslist)

### 版本：
  
|名称|版本|说明|
|:-|:-|:-|
|qBittorrent|qee_4.1.9.15|增强版 (amd64)|


### 注意：

1. qBittorrent-Enhanced-Edition 增强版 需下载对应版本ipfilter.dat放入qBittorrent配置文件夹才能屏蔽离线下载 [https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases](https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases)

## 关于群晖

群晖用户请使用你当前的用户SSH进系统，输入 ``id 你的用户id`` 获取到你的UID和GID并输入进去

![](https://github.com/SuperNG6/pic/blob/master/baidupcs/Xnip2019-12-19_17-18-20.png)
![](https://github.com/SuperNG6/pic/blob/master/baidupcs/Xnip2019-12-19_17-18-11.png)
![](https://github.com/SuperNG6/pic/blob/master/baidupcs/Xnip2019-12-19_17-23-27.png)

### 权限管理设置
对你的``docker配置文件夹的根目录``进行如图操作，``你的下载文件夹的根目录``进行相似操作，去掉``管理``这个权限，只给``写入``,``读取``权限
![](https://github.com/SuperNG6/pic/blob/master/aria2/Xnip2019-12-07_10-35-24.png)

### docker命令行设置：


1. 创建qbittorrent容器

````
docker create  \
    --name=qbittorrentee  \
    -e WEBUIPORT=8080  \
    -e PUID=1026
    -e PGID=100
    -e TZ=Asia/Shanghai
    -p 6881:6881  \
    -p 6881:6881/udp  \
    -p 8080:8080  \
    -v /配置文件位置:/config  \
    -v /下载位置:/downloads  \
    --restart unless-stopped  \
    superng6/qbittorrent:latest
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
      - /path/to/downloads:/downloads
    ports:
      - 6881:6881
      - 6881:6881/udp
      - 8080:8080
    restart: unless-stopped
````



### 变量:

|参数|说明|
|-|:-|
| `--name=qbittorrentee` |容器名|
| `-p 8080:8080` |web访问端口 [IP:8080](IP:8080);(默认用户名:admin;默认密码:adminadmin);此端口需与容器端口和环境变量保持一致，否则无法访问|
| `-p 6881:6881` |BT下载监听端口|
| `-p 6881:6881/udp` |BT下载DHT监听端口
| `-v /配置文件位置:/config` |qBittorrent配置文件位置|
| `-v /下载位置:/downloads` |qBittorrent下载位置|
| `-e WEBUIPORT=8080` |web访问端口环境变量|
| `-e TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|

### 群晖docker设置：

1. 卷

|参数|说明|
|-|:-|
| `本地文件夹1:/downloads` |qBittorrent下载位置|
| `本地文件夹2:/config` |qBittorrent配置文件位置|

2. 端口

|参数|说明|
|-|:-|
| `本地端口1:6881` |BT下载监听端口|
| `本地端口2:6881/udp` |BT下载DHT监听端口|
| `本地端口3:8080` |web访问端口 [IP:8080](IP:8080);(默认用户名:admin;默认密码:adminadmin);此端口需与容器端口和环境变量保持一致，否则无法访问|

3. 环境变量：

|参数|说明|
|-|:-|
| `TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|
| `WEBUIPORT=8080` |web访问端口环境变量|

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
