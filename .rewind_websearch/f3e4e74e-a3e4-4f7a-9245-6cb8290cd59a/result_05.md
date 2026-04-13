# 排查克隆错误-<em>GitHub</em> Docs

URL: https://docs.github.com/zh/enterprise-server@3.12/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors

Query: GitHub Pages 404 error troubleshooting user-research123 repository

---

管理提交签署策略
管理推送策略
匿名Git 读取权限
用于推送的电子邮件通知
配置自动链接
标记保护规则
Manage auto-closing issues
分支和合并
管理分支
查看分支
重命名分支
更改默认分支
删除和还原分支
配置 PR 合并
关于合并方法
配置提交合并
配置提交压缩
配置提交变基
管理合并队列
管理分支更新
管理自动合并
自动删除分支
管理受保护的分支
关于受保护分支
分支保护规则
管理规则集
关于规则集
创建规则集
管理规则集
可用规则
故障排除
处理文件
管理文件
创建新文件
添加文件
移动文件
编辑文件
重命名文件
删除文件
更改文件的显示方式
使用文件
查看并了解文件
文件的永久链接
源代码存档
使用非代码文件
管理大型文件
大型文件
Git Large File Storage
安装 Git LFS
配置 Git LFS
协作
移动文件到 Git LFS
“删除文件”
解决上传失败
发布项目
关于发行版
管理版本
查看版本和标记
搜索版本
链接到发行版
比较发行版
自动发行说明
自动发布表单
查看活动和数据
查看部署活动
关于仓库图
使用 Pulse
查看项目贡献者
分析更改
存储库之间的连接
使用活动视图
存档存储库
存档仓库
备份仓库
此版本的 GitHub Enterprise Server 已于以下日期停止服务 2025-04-03 . 即使针对重大安全问题，也不会发布补丁。 为了获得更好的性能、更高的安全性和新功能，请 升级到最新版本的 GitHub Enterprise 。 如需升级帮助，请 联系 GitHub Enterprise 支持 。
创建和管理存储库 / 
排查克隆错误
如果您在克隆存储库时遇到问题，请检查这些常见错误。
本文内容
HTTPS 克隆错误
错误：未找到仓库
错误：远程 HEAD 引用不存在的 ref，无法检出
HTTPS 克隆错误
对 Git 使用 HTTPS 时有几种常见错误。 这些错误通常表示您有旧版 Git，或无法访问仓库。
下面是您可能收到的 HTTPS 错误示例：
>  error: The requested URL returned error: 401  while  accessing >  https://HOSTNAME/USER/REPO.git/info/refs?service=git-receive-pack >  fatal: HTTP request failed
>  Error: The requested URL returned error: 403  while  accessing >  https://HOSTNAME/USER/REPO.git/info/refs >  fatal: HTTP request failed
>  Error: https://HOSTNAME/USER/REPO.git/info/refs not found: did you run git >  update-server-info on the server?
检查 Git 版本
与 GitHub 交互没有最低 Git 版本要求，但我们发现 1.7.10 版是一个方便、稳定的版本，适用于许多平台。 你可以始终在  Git 网站上下载最新版本 。
确保远程正确
正在尝试提取的仓库必须存在于 你的 GitHub Enterprise Server 实例 上。
可以打开命令行并键入  git remote -v  来查找本地存储库的 URL：
$  git remote -v #  View existing remotes >  origin  https://github.com/ghost/cocoareactive.git (fetch) >  origin  https://github.com/ghost/cocoareactive.git (push)  $  git remote set-url origin https://github.com/ghost/ReactiveCocoa.git #  Change the  'origin'  remote 's URL  $  git remote -v #  Verify new remote URL >  origin  https://github.com/ghost/ReactiveCocoa.git (fetch) >  origin  https://github.com/ghost/ReactiveCocoa.git (push)
也可通过  GitHub Desktop  应用程序更改 URL。
提供访问令牌
要访问 GitHub，你必须使用 personal access token 而不是密码进行身份验证。 有关详细信息，请参阅“ 管理个人访问令牌 ”。
检查权限
提示输入用户名和密码时，确保使用可以访问仓库的帐户。
Tip
 如果不想在每次与远程存储库交互时都输入用户名和密码，可以打开 凭据缓存 。 如果已在使用凭据缓存，请确保您的计算机缓存了正确的凭据。 不正确或过期的凭据将导致身份验证失败。
改用 SSH
如果您以前设置了 SSH 密钥，便可使用 SSH 克隆 URL，而不使用 HTTPS。 有关详细信息，请参阅“ 关于远程仓库 ”。
错误：未找到仓库
如果在克隆存储库时看到此错误，这意味着存储库不存在或者你无权访问它，或者 你的 GitHub Enterprise Server 实例 处于专用模式。 此错误有一些解决方案，具体取决于错误原因。
检查拼写
发生拼写错误。 如果尝试克隆  git@HOSTNAME:owner/repotile.git ，但存储库已实际命名为  owner/repoti1e ，则会收到此错误。
要避免此错误，克隆时，始终从仓库页面复制和粘贴克隆 URL。 有关详细信息，请参阅“ 克隆仓库 ”。
若要更新现有仓库上的远程存储，请参阅  管理远程仓库 。
检查权限
如果您尝试克隆私有仓库，但没有查看仓库的权限，您将收到此错误。
确保您通过以下方式之一中，拥有仓库的访问权限：
仓库所有者 存储库上的 协作者 拥有存储库访问权限的 团队成员 （如果存储库属于组织）
检查 SSH 访问权限
在极少数情况下，您可能没有仓库的适当 SSH 访问权限。
应确保正在使用的 SSH 密钥已连接到你在 GitHub 上的个人帐户。 可以通过在命令行中键入以下内容检查此项：
$  ssh -T git@HOSTNAME >  Hi USERNAME! You 've successfully authenticated, but GitHub does not >  provide shell access.
有关详细信息，请参阅“ 将新的 SSH 密钥添加到 GitHub 帐户 ”。
检查实例是否处于私有模式
如果站点管理员已对你的 GitHub Enterprise 实例启用专用模式，将禁用通过  git://  进行的匿名克隆。 如果您无法克隆仓库，请联系您的站点管理员。
检查仓库...
