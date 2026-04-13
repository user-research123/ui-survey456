# <em>Flask</em> 项目在<em>阿里云</em>上的完整<em>部署</em>指南-CSDN博客

URL: https://m.blog.csdn.net/qq_38444844/article/details/154574970

Query: 阿里云函数计算 FC 部署 Python Flask 教程 2025 2026

---

python  - flask 项目开发部署：
完整开发实战总结：https://blog.csdn.net/qq_38444844/article/details/151928286?spm=1011.2415.3001.5331 项目源码：https://gitee.com/loveTianWen/Forum-platform/tree/master Flask 项目部署阿里云技术大纲：https://blog.csdn.net/qq_38444844/article/details/154584891?spm=1011.2415.3001.5331 Ansible 实现自动化多机部署Flask 项目（完整过程总结）:https://blog.csdn.net/qq_38444844/article/details/155381768?sharetype=blogdetail&sharerId=155381768&sharerefer=PC&sharesource=qq_38444844&spm=1011.2480.3001.8118 从ECS云服务器到 Gitee + Docker + ACR：Flask 项目全链路部署记录：https://blog.csdn.net/qq_38444844/article/details/156300164?sharetype=blogdetail&sharerId=156300164&sharerefer=PC&sharesource=qq_38444844&spm=1011.2480.3001.8118
详细图文部署教程（Flask on 阿里云轻量 服务器 ）
阿里云轻量应用服务器（Lighthouse）
 系统环境：Alibaba Cloud Linux 3（兼容 CentOS/RHEL 8），不兼容 Ubuntu
 应用镜像： WordPress 6.8.3 已卸载
 Web 框架：Flask + Gunicorn + Nginx
 数据库：MariaDB（MySQL 兼容）
 部署方式：systemd + Unix Socket
 记录时间：2025 年 11 月
注意事项：
这个镜像是为 WordPress 定制的，已预装 Apache/Nginx + PHP + MySQL，并占用了 80/443端口！ 如果部署 Python Flask 项目，不能直接覆盖 WordPress，否则会导致端口、服务、配置混乱冲突。 保留系统，卸载 WordPress 相关组件，重新部署 Flask， 轻量服务器本质仍是ECS，只是预装了应用。“清空”WordPress 环境，当作纯净centos 使用。
不同系统工具包名
 Ubuntu：apt
 centos/Red Hat：yum 或 dnf
cat /etc/os-release：查看系统版本信息
# 系统版本 NAME = "Alibaba Cloud Linux" VERSION = "3 (OpenAnolis Edition)" ID = "alinux" ID_LIKE = "rhel fedora centos anolis" VERSION_ID = "3" VARIANT = "OpenAnolis Edition" VARIANT_ID = "openanolis" ALINUX_MINOR_ID = "2104" ALINUX_UPDATE_ID = "12" PLATFORM_ID = "platform:al8" PRETTY_NAME = "Alibaba Cloud Linux 3.2104 U12 (OpenAnolis Edition)" ANSI_COLOR = "0;31" HOME_URL = "https://www.aliyun.com/"
AI写代码 bash
1 2 3 4 5 6 7 8 9 10 11 12 13 14
服务器选购：
 1、登录阿里云官网：https://cn.aliyun.com/
 2、进入 ECS 控制台
搜索 “轻量应用服务器” → 点击进入
3、创建实例（推荐配置）
一、部署前准备
1.登录服务器（SSH）
方法 1：使用阿里云控制台「远程连接」进入 轻量应用服务器控制台 找到你的实例 → 点击 “远程连接”输入用户名 root 和你设置的密码
方法 2：本地终端 SSH（推荐）
ssh  root@你的公网IP 
AI写代码 bash
1
2.停止并卸载 WordPress 及其依赖（释放 80 端口）
停止 Apache（WordPress 默认用 Apache）
sudo  systemctl stop apache2  sudo  systemctl disable apache2 
AI写代码 bash
1 2
卸载 Apache、PHP、WordPress（可选，但推荐）
 此时 80 端口已空闲！
sudo apt  remove --purge apache2 php* wordpress -y  sudo apt  autoremove -y 
AI写代码 bash
1 2
（可选）清理残留文件
sudo rm  -rf /var/www/html/ 
AI写代码 bash
1
3. 服务器初始化
使用阿里云轻量应用服务器，选择  Alibaba Cloud Linux 3  镜像 开放安全组端口： 22 （SSH）、 80 （HTTP）、 443 （HTTPS） 更新系统：
# -y自动确认 sudo  dnf update -y  && sudo apt  update 
AI写代码 bash
1 2
4. 安装必要软件包
Alibaba Cloud Linux 3 使用 dnf 作为包管理器（类似 CentOS 8）， \ 是 Bash（Linux shell）中的“行继续符”
sudo  dnf  install  -y  git  python3 python3-pip python3-devel \   mariadb-server mariadb gcc nginx 
AI写代码 bash
1 2
5. 验证
python3 --version    # 应 ≥ 3.10  nginx -v             # 应显示版本
AI写代码 bash
1 2
二、部署步骤详解
1. 上传你的 Flask 项目
如果没有 Git 仓库，可用 scp 或 FinalShell / WinSCP 上传文件夹
cd  /home  # 克隆代码 git  clone https://gitee.com/yourname/Forum-platform.git    cd  Forum-platform 
AI写代码 bash
1 2 3 4 5 6
2. 创建 Python 虚拟环境并安装依赖
# 创建虚拟环境  python3 -m venv venv   # 激活 source  venv/bin/activate   # 安装依赖（确保项目根目录有 requirements.txt） 包...
