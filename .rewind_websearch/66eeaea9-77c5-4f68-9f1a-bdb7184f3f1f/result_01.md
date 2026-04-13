# 安全的<em>流量加速</em>-Citrix Product Documentation

URL: https://docs.citrix.com/zh-cn/citrix-sd-wan-wanop/current-release/secure-traffic-acceleration.html

Query: "Dogfooding" 加速器 流量限制

---

CIFS 和 MAPI
压缩
RPC over HTTPS
SCPS
安全对等
SSL 加速
Citrix SD-WAN WANOP 插件
流量成形
升级
视频缓存
Office 365 加速
 压缩 
 HTTP 加速 
 HTML5 的工作原理 
 互联网协议版本 6 (IPv6) 加速 
 链接定义 
管理流量成形中的链接定义
配置链接定义
 使用 Citrix Application Delivery Management 管理和监视 
 Citrix Cloud Connector 
配置 Cloud Connector 隧道
配置两个数据中心之间的 Cloud Connector 隧道
配置数据中心和 AWS/Azure 之间的 Cloud Connector 隧道
 Office 365 加速 
 SCPS 支持 
 安全的流量加速 
安全对等
CIFS、SMB2 和 MAPI
 配置 Citrix SD-WAN WANOP 设备以优化安全的 Windows 流量 
 配置 CIFS 和 SMB2/SMB3 加速 
 配置 MAPI 加速 
SSL 压缩
 SSL 压缩的工作原理 
 配置 SSL 压缩 
 使用 Citrix SD-WAN WANOP 插件进行 SSL 压缩 
RPC over HTTP
 TCP 流量控制加速 
无损透明流量控制
速度优化
自动发现和自动配置
TCP 流量控制模式
防火墙注意事项
 流量分类 
应用程序分类器
服务类别
 流量成形 
加权公平排队
流量成形策略
 视频缓存 
视频缓存场景
配置视频缓存
视频预填充
验证视频缓存
管理视频缓存源
 WAN 见解 
 非对称路由 
 Citrix SD-WAN WANOP 客户端插件 
硬件和软件要求
WANOP 插件的工作原理
部署用于插件的设备
自定义插件的 MSI 文件
在 Windows 上部署插件
Citrix SD-WAN WANOP 插件
更新 Citrix SD-WAN WANOP 插件
 Virtual Apps and Desktops 加速 
配置虚拟应用程序加速
优化 Citrix Receiver for HTML5
部署模式
自适应传输互操作性
 Citrix Hypervisor 6.5 升级 
 维护 
 诊断 
 故障排除 
CIFS 和 MAPI
Citrix SD-WAN WANOP 插件
RPC over HTTPS
视频缓存
Virtual Apps and Desktops 加速
 文档历史记录 
Citrix SD-WAN WANOP Citrix SD-WAN WANOP 11.3
通过安全对等来实现安全的流量接入。若干高级功能要求链接两端的 Citrix SD-WAN WANOP 设备建立彼此之间的  安全对等关系  ，从而设置 SSL 信令隧道（也称为  信令连  接）。这些 功能包括 SSL 压缩、签名 CIFS 支持和加密 MAPI 支持。
启用安全对等后，对于尚未与本地设备建立安全对等关系的所有伙伴设备（以及运行 Citrix SD-WAN WANOP 插件的计算机），将自动禁用压缩。
要建立安全对等关系，您必须生成安全密钥和证书，并在设备之间配置安全信号隧道。在配置隧道之前，请从 Citrix 订购加密许可证。
NetScaler 
This Preview product documentation is  Cloud Software Group  Confidential. 
You agree to hold this documentation confidential pursuant to the terms of your  Cloud Software Group  Beta/Tech Preview Agreement. 
The development, release and timing of any features or functionality described in the Preview documentation remains at our sole discretion and are subject to change without notice or consultation.
The documentation is for informational purposes only and is not a commitment, promise or legal obligation to deliver any material, code or functionality and should not be relied upon in making  Cloud Software Group  product purchase decisions. 
If you do not agree, select I DO NOT AGREE to exit.
