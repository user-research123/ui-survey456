# hexo结合<em>github</em>制作个人网页过程中<em>error</em>记录与解决-CSDN博客

URL: https://m.blog.csdn.net/qq_45698889/article/details/144775888

Query: GitHub Pages 404 error troubleshooting user-research123 repository

---

原本是打算写整个流程的，但是网上制作流程很详细的，所以我就不多此一举了，直接列出过程中遇到的error与解决方法供后来者参考。
1.  hexo  deployer（简化hexo d）出错Error：Spawn failed
Spawn failed 是一个综合性问题，很多情况都会触发，以下列出我所遇到的两种情况以及解决方法
1.1 科学上网导致ssh连接不到库
ssh: connect to host github.com port 22: Connection timed out
fatal: Could not  read  from remote repository.
Please make sure you have the correct access rights
and the repository exists.
FATAL Something’s wrong. Maybe you can find the solution here: https://hexo.io/docs/troubleshooting.html
Error: Spawn failed
at ChildProcess. (D:\Myblog\myblog\node_modules\hexo-util\lib\spawn.js:51:21)
at ChildProcess.emit (events.js:314:20)
at ChildProcess.cp.emit (D:\Myblog\myblog\node_modules\cross-spawn\lib\enoent.js:34:29)
at Process.ChildProcess._handle.onexit (internal/child_process.js:276:12)
智能体编程 bash
因为国内众所周知的情况，大家要访问 github 肯定要科学上网，如果在hexo init的时候没有科学上网或者使用 加速器 ，但是为了看hexo是否上传成功肯定又要科学上网或使用加速器。这IP变换的过程就会导致hexo d的时候ssh连接不到
这种情况就很好解决了，保持hexo init和hexo d的时候IP地址一致就好了。
1.2 git进行push或者hexo d的时候改变了一些.deploy_git文件下的内容。
INFO  Validating config
INFO  Start processing
INFO  Files loaded  in  145 ms
INFO  Generated: archives/index.html
INFO  Generated: index.html
INFO  Generated: css/style.css
INFO  Generated: fancybox/jquery.fancybox.min.css
INFO  Generated: js/script.js
INFO  Generated: archives/2024/12/index.html
INFO  Generated: fancybox/jquery.fancybox.min.js
INFO  Generated: js/jquery-3.6.4.min.js
INFO  Generated: archives/2024/index.html
INFO  Generated: css/images/banner.jpg
INFO  Generated: 2024/12/24/Christmas-Eve/index.html
INFO  Generated: 2024/12/23/hello-world/index.html
INFO  Generated: 2024/12/23/12-23-record/index.html
INFO  13 files generated  in  366 ms
INFO  Deploying: git
INFO  Setting up Git deployment...
Initialized empty Git repository  in  D:/myblog/.deploy_git/.git/
[master (root-commit) b991765] First commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 placeholder
INFO  Clearing .deploy_git folder...
INFO  Copying files from public folder...
INFO  Copying files from extend  dirs ...
warning:  in  the working copy of  '2024/12/23/12-23-record/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  '2024/12/23/hello-world/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  '2024/12/24/Christmas-Eve/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  'archives/2024/12/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  'archives/2024/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  'archives/index.html' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  'css/style.css' , LF will be replaced by CRLF the next time Git touches it
warning:  in  the working copy of  'fancybox/jquery.fancybox.min.js' , LF will be replaced by CRLF the n...
