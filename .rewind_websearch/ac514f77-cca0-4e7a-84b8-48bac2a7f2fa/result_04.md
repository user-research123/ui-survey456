# 写一篇漂亮的技术调研文档-少数派

URL: https://sspai.com/post/101777

Query: user-research123.github.io wangzhe_report 闲鱼 4月10日

---

平时逛 Github 或者 NPM 网站时候，在 README.md 中或多或少都会看到一些这样的图标：
在枯燥的文档中加入这样的图标能让文档的观感提升不少，且可以增加读者的信任度。
读者会认为这份文档你是认真写的，且看着 比较专业 。
认真  +  专业  =  信任      
原理
这些图标除了精美之外，它所展示的数据是实时的，这就非常酷了。
它让你文档呈现的数据永远都是准确的。
原理也较为简单，我们来解析一下这个路径：
https://img.shields.io/github/stars/vuejs/core?color=white&label
它就是往  img.shields.io  这个服务器请求图片，通过一定规则拼装出请求参数，让服务器知道我们需要什么数据。
示例的地址就是告诉服务器返回一张  表示 vue 仓库的 star 数量的图片
而这样的雷锋服务器目前我知道的有3个：
shields.io/  支持多种图标 flat.badgen.net/  支持多种图标 packagephobia.com/  只返回指定 npm 包所占用的内存大小
这些服务器会根据我们的请求参数，去获取数据源，将数据包装成一个漂亮的图标，返回给客户端。
我也想高大上
之前逛 NPM 的时候发现  got  这个包的 README.md 非常精美。作者列举了该库和其他类似库的一些对比数据，觉得非常专业。
看着是一个小图标，但是它展示的数据却是实时的、动态的
于是我在写调研报告的时候也学着写了一个这样的表格：
截图是之前写的技术调研报告
表格看着是很舒服，可是编辑 markdown 的时候费了老命了。短短的一张对比表格，需要配置这么多的图片地址和图片链接，配置完了还得保证组合正确，瞬间觉得投入产出不成正比了。（除非写这样的报告可以拿奖金，否则不可能再写第二次！！）
如下文本是上面那张表格的 markdown 源码，来感受一下工作量：
## npm 包对比   |                    |    [ `yauzl` ][ ygit ]    | [ `extract-zip` ][ egit ] |   [ `adm-zip` ][ agit ]   |  [ `unzipper` ][ ugit ]   |   [ `archiver` ][ argit ]   | | ------------------ | :-------------------: | :-------------------: | :-------------------: | :-------------------: | :---------------------: | | Issues open        |   [ ![ ][ yio ]][ yio_a ]   |   [ ![ ][ eio ]][ eio_a ]   |   [ ![ ][ aio ]][ aio_a ]   |   [ ![ ][ uio ]][ uio_a ]   |   [ ![ ][ ario ]][ ario_a ]   | | Issues closed      |   [ ![ ][ yic ]][ yic_a ]   |   [ ![ ][ eic ]][ eic_a ]   |   [ ![ ][ eic ]][ aic_a ]   |   [ ![ ][ uic ]][ uic_a ]   |   [ ![ ][ aric ]][ aric_a ]   | | Downloads          |    [ ![ ][ yd ]][ yd_a ]    |    [ ![ ][ ed ]][ ed_a ]    |    [ ![ ][ ad ]][ ad_a ]    |    [ ![ ][ ud ]][ ud_a ]    |    [ ![ ][ ard ]][ ard_a ]    | | Bugs               |  [ ![ ][ ybug ]][ ybug_a ]  |  [ ![ ][ ebug ]][ ebug_a ]  |  [ ![ ][ abug ]][ abug_a ]  |  [ ![ ][ ubug ]][ ubug_a ]  |  [ ![ ][ arbug ]][ arbug_a ]  | | Dependents         |   [ ![ ][ ydp ]][ ydp_a ]   |   [ ![ ][ edp ]][ edp_a ]   |   [ ![ ][ adp ]][ adp_a ]   |   [ ![ ][ udp ]][ udp_a ]   |   [ ![ ][ ardp ]][ ardp_a ]   | | Install size       | [ ![ ][ ysize ]][ ysize_a ] | [ ![ ][ esize ]][ esize_a ] | [ ![ ][ asize ]][ asize_a ] | [ ![ ][ usize ]][ usize_a ] | [ ![ ][ arsize ]][ arsize_a ] | | GitHub stars       |  [ ![ ][ ystar ]][ ygit ]   |  [ ![ ][ estar ]][ egit ]   |  [ ![ ][ astar ]][ agit ]   |  [ ![ ][ ustar ]][ ugit ]   |  [ ![ ][ arstar ]][ argit ]   | | TypeScript support |   [ ![ ][ yts ]][ ygit ]    |   [ ![ ][ ets ]][ egit ]    |   [ ![ ][ ats ]][ agit ]    |   [ ![ ][ uts ]][ ugit ]    |   [ ![ ][ arts ]][ argit ]    | | Last commit        |   [ ![ ][ ycm ]][ ycm_a ]   |   [ ![ ][ ecm ]][ ecm_a ]   |   [ ![ ][ acm ]][ acm_a ]   |   [ ![ ][ ucm ]][ ucm_a ]   |   [ ![ ][ arcm ]][ arcm_a ]   | | symlink support    |  :heavy _check_ mark:   |  :heavy _check_ mark:   |          :x:          |      :question:       |       :question:        |  <!-- https://gist.github.com/rxaviers/7360908 图标编码参考 -->  <!-- GITHUB -->  [ ygit ]:  https://github.com/thejoshwolfe/yauzl  ...
