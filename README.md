## 物联网河道水位集中监控平台zh_CN

### 目录

[toc]
### 项目简介
#### 概述
本项目是基于超声波距离传感器、RS485串口透传模块的物联网应用平台。  
平台集采集、回放、预警为一体，综合了水位数据和实况视频；支持多站部署、单站多传感器部署；不受网络环境限制，可应对有线网络、4G网络、NB-IoT等各种复杂情况。响应式页面，在手机和电脑端查看均有较好体验。  
平台理论上支持各种距离传感器、串口服务器、摄像头、NVR等设备。本次安装采用```深圳电应普A16-485超声波距离传感器```、```塔石TS-LAN-460串口服务器```，视频监控部分使用```极路由HC5761A```反向代理。

#### 使用效果

![APP样机展示2](https://raw.githubusercontent.com/BaiHLiu/images/master/img/APP%E6%A0%B7%E6%9C%BA%E5%B1%95%E7%A4%BA2.jpg)

![APP样机展示1](https://raw.githubusercontent.com/BaiHLiu/images/master/img/APP%E6%A0%B7%E6%9C%BA%E5%B1%95%E7%A4%BA1.jpg)

### 产品特性

#### 用户功能
+ 水位即时显示
> 在首页显示各个站点、各个传感器的实时参数。包括水位、水深、温度、更新时间、在线状态，轮询上报时间可设置。
+ 历史记录和图表查询
> 首页默认显示所有站点8小时历史记录，历史页面可自定义开始、结束时间查询。
+ 实况抓图监控
> 默认每10分钟抓取一张全尺寸摄像头图片，直观清晰。
+ 水情日报表生成
> 生成供单位上报的各站点即时参数。
+ 微信报警推送
> 扫描二维码可订阅报警消息。
#### 管理功能
+ 水位和水深自助校准
> 登录管理员账号后，可在设备页面校准设备。只需要输入当前实际水位和底板海拔高度，系统会保存并自动计算。
+ 串口服务器的添加和配置
> 可配置串口服务器（站点）名称、本地端口号、轮询周期、读取距离和温度值的Modbus485指令。
+ 传感器的添加和配置
> 可配置各站点传感器的名称、485设备16进制地址码。
+ 报警参数设置
> 支持```高低超限```和```变化速率```超限两种报警策略，参数可据实际需要自由设置。
### 部署说明
#### 基本知识
使用和开发该项目，您需要掌握以下概念：
+ Socket基础知识
+ Modbus485串口通信（地址码、寄存器、CRC校验）
+ Flask
+ SQLite
+ RTSP
+ RTSP
+ jQuery

您需要参考以下内容：  
[WxPusher消息推送服务](https://wxpusher.zjiecode.com/docs/#/)  
[FRP反向代理](https://github.com/fatedier/frp)  
[Apache ECharts](https://echarts.apache.org/zh/index.html)  
[openCV connect RTSP stream](https://answers.opencv.org/question/230143/opencv-connect-and-process-an-ip-camera-stream-rtsp-protocol/)

#### 目录结构
```text
.
├── httpAPI/                    # 用于tcpServer上报消息和获取参数
├── imageCapture/               # 用于rtsp视频监控抓图存储
├── msgPush/                    # 微信消息推送组件
├── tcpServer/                  # socket服务器，用于物联网设备的注册和数据上报
├── test/                       # 供tcp通信测试
├── webApp/                     # 基于flask的web后端
├── conf_default.py             # python全局配置类
├── db_default.sql              # sqlite数据库结构
└── requirements.txt            # 依赖文件
```
#### 快速部署
1. 安装依赖  
进入源码包目录，执行命令
```shell
python3 -m pip update
python3 -m pip install -r requirements.txt
```
2. 修改配置  
注：修改后将"_default"去掉即可。
+ **/conf_default.py**
    + tcp_server：用于物联网设备socket通信、上报数据的服务器配置，其中```http_api_endpoint```需要填写http_api的实际地址。
    + http_api：用于tcp_server上报消息和获取传感器请求参数。
    + web_app：Flask后端运行配置。
    + msg_push：微信推送设置，基于WxPusher，详情请见官方文档。
    + user：普通用户和管理员账户密码，因暂无多用户需求，故直接将用户信息保存在配置文件中。
+ **/webApp/pages/js/config_default.js**  
设置webApp后端服务器地址。
+ **/imageCapture/camConf_default.py**  
设置rtsp抓图地址。
+ **/webApp/rt_report.py**  
用于生成即时报表，请修改76行的文件保存路径。  
**警告**：禁止将网站服务器根目录设置在**本项目的任何位置**，请务必另选存储位置，并设置好相关权限。

3. 运行  
依次运行```/httpApi/app.py```、```/tcpServer/tcp-server.py```、```/webApp/app.py```
```/imageCapture/rtsp.py```负责抓图功能，请使用合适的方法定时运行，建议10分钟执行一次。

### 开发指南
若您需要对该项目二次开发，我给出以下几点提示。  
1. 项目中的概念：485透传模块可称为"设备"、"站点"、"串口服务器"；传感器即为"传感器"。
2. 由于历史记录的算法不是很好，为了确保不出问题，轮询周期不可超过1分钟，建议10s-30s。
3. 若采用本项目所用的硬件，可参考```/docs```目录下的传感器、串口服务器开发手册。
### TODO  
1. 优化历史记录算法。
2. 添加自定义rtsp视频URL。
3. 优化报警算法：允许给单个传感器单独设置报警参数、同一警型仅提示一次，而不是使用时间间隔控制。