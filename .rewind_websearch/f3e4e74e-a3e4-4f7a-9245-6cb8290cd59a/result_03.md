# Hugo + <em>GitHub</em> <em>Pages</em> 部署 <em>404</em> 踩坑全记录（超详细避坑指南）-CSDN博客

URL: https://m.blog.csdn.net/weixin_43664184/article/details/158617126

Query: GitHub Pages 404 error troubleshooting user-research123 repository

---

Hugo + GitHub Pages 部署 404 踩坑全记录（附简略安装指南+超详细避坑指南）
看了大家的帖子发现很多人，一直 404。
 整理一下最容易踩的几个坑，帮后来人少走弯路。
一. 安装
 1.到 https://gohugo.io/ 后点图片的第一步 Github里面的tag去下载最新版本去解压
二. 下载主题
 1.主题Themes也是一样 进入后下载到你本地
三. 提交到GitHub
 1.先去cmd 在你的hugo路径下 “hugo -D” 启动项目后，看看文件夹你的hugo路径下的public的时间是不是启动时间，时间对的话，就把public的文件全部push到你的github仓库去
 大部分博主用git复制指令去推送代码，我这里用的可视化工具GitHub window版本去推也是一样的，
坑点一  注意，是public里面的文件，不包含public，不然你的配置错了读不到public
 以下是github desktop的提交步骤，summary这个摘要一定要填写后才能提交，这也是开发中规范流程，记录你每次提交的缘由
 推上去后确认下你的仓库路径是否如下
 很多人的仓库结构是这样的：
你的仓库
 └── public
 ├── index.html
 GitHub Pages 读取的是仓库根目录
 正确路径是： （不然404
你的仓库
 ├── index.html
 ├── posts
 ├── css
 ├── js
这一步没问题的话 进入
坑点二
 baseURL 写错（最常见）
 hugo 文件里面的配置文件yml 中第一行的baseURL中
 必须要改成你仓库的地址！！！！
 baseURL: “https://用户名.github.io/仓库名/”
 注意三点：
 必须是真实访问路径
 必须带双引号
 必须带最后的 /
否则：
 CSS 路径错误
 资源加载失败
 直接 404
坑点三
 Pages 设置错目录（你的github 的setting那里
 必须是：
 Source: Deploy from branch
 Branch: main
 Folder: /(root)
如果选成 / docs  会 404
四、最终总结
Hugo + GitHub Pages 出现 404，基本只可能是：
baseURL 错
push 目录结构错
Pages 目录选错
只要这三点对了，一定能成功。
