# Python<em>爬虫</em>实战：30分钟搞定在线考试题库抓取，附反爬突破+<em>结构</em>化存储（程序员专属干货）-CSDN博客

URL: https://m.blog.csdn.net/shanwei_spider/article/details/156614807

Query: pxb7.com 螃蟹账号平台 爬虫 数据结构

---

最近准备软考（系统集成项目管理工程师），需要大量真题和模拟题来刷题。但找了好几个在线题库平台，要么需要付费解锁，要么只能在线做没法导出打印，想整理成错题本都难。作为程序员，肯定不能手动复制粘贴——花了1个晚上写了个Python爬虫，直接批量抓取了上千道题库真题，还整理成了带解析的Excel表格。今天把完整实战过程拆解出来，从抓包分析到反爬突破，再到程序员喜欢的标题生成，全是亲测有效的干货，帮有考证、刷题需求的小伙伴省时间。
先聊真实需求：程序员刷题的核心痛点
不管是软考、PMP、教资还是编程语言认证，程序员刷题都有几个共性痛点：
在线题库无法导出，想离线刷题、整理错题都不方便； 付费题库成本高，很多平台按科目收费，少则几十多则上百； 手动整理效率低，一道题复制题干、选项、答案、解析，10道题就要半小时； 想针对性刷题（比如只刷编程题、案例题），平台筛选功能不精准。
我的核心目标很明确： 批量抓取指定题库的完整题目信息（题干+选项+答案+解析+题型），结构化存储到Excel，支持按题型/考点筛选，全程避开反爬机制 。
技术选型：实用优先，拒绝过度设计
作为每天写业务代码的程序员，我选技术的原则是“轻量、灵活、好调试”，没必要为了简单的题库抓取上Scrapy这种重框架。最终确定的技术栈如下（附真实选型理由）：
requests + Session ：保持登录会话，应对题库平台的Cookie验证（很多平台未登录只能看10道题，登录后才能看完整题库）； fake-useragent ：生成随机User-Agent，避免固定UA被平台识别为爬虫； parsel ：解析HTML页面，用XPath/CSS选择器提取题目信息，比正则表达式直观，调试起来更方便； pandas ：结构化存储数据，直接导出Excel，后续筛选、排序都方便； lxml ：增强HTML解析稳定性，部分题库页面标签嵌套混乱，lxml解析效率更高。
环境安装命令（Python3.7+均可，亲测3.9、3.10无问题）：
pip  install  requests fake-useragent parsel pandas lxml 
AI写代码 bash
1
第一步：抓包分析——题库爬虫的核心前置工作
想抓题库，先搞懂平台的请求逻辑，这一步没做好，后面全白搭。我以某热门在线题库平台（避免广告，用“目标平台”代称）为例，步骤如下：
打开浏览器（Chrome）→ F12打开开发者工具 → 切换到「Network」面板，筛选「Doc」类型； 登录目标平台，进入软考真题题库页面，刷新页面，找到返回题库列表的主请求（URL通常包含“exam”“question”“bank”等关键词）； 点击“下一页”，观察请求参数变化——发现平台用 page （页码）、 limit （每页条数）、 subject_id （科目ID）三个核心参数控制分页； 点击某道题进入详情页，观察详情页URL结构： https://xxx.com/question/detail?id=xxx ，其中 id 是题目唯一标识； 关键验证：用浏览器“复制请求头”，在Postman里模拟请求，能正常返回页面则说明无复杂加密（如果返回403/500，可能需要处理sign参数或Token，后面会讲）。
踩坑前置：常见题库平台反爬手段
根据我的经验，在线题库的反爬不算极端，但这3个点要重点注意：
未登录限制：未登录只能查看少量题目，必须模拟登录或携带有效Cookie； UA验证：固定UA请求10次左右就会被限制，需要随机切换； 请求频率：短时间内大量请求会被封IP，需添加随机延时。
第二步：核心代码实现——从登录到抓取全流程
我把代码拆成4个模块化类，方便后续复用和修改，每一步都带详细注释，直接复制就能运行。
1. 基础配置与登录封装（应对登录验证）
很多题库需要登录才能查看完整题目，这里提供两种方案：手动复制Cookie（适合新手）、模拟登录（适合需要长期抓取的场景），我用手动复制Cookie的方案，简单高效。
import  requests  import  time  import  random  from  fake_useragent  import  UserAgent  from  parsel  import  Selector  import  pandas  as  pd   # 基础配置类：封装会话、请求头、延时、代理 class ExamCrawlerConfig : def __init__ ( self ,  cookie_str ) : # 初始化Session，保持登录态          self . session  =  requests . Session ( ) # 随机User-Agent          self . ua  =  UserAgent ( ) # 基础请求头          self . headers  = { "User-Agent" :  self . ua . random , "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" , "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8" , "Accept-Encoding" : "gzip, deflate, br" , "Connection" : "keep-alive" , "Upgrade-Insecure-Requests" : "1" , "Cookie" :  cookie_str   # 手动复制的Cookie }          self . session . headers . update ( self . headers ) # 代理池（可选，免费代理不稳定，付费代理更靠谱，这里仅示例）          self . proxy_pool  = [ "http://121.xxx.xxx.xxx:8080" , "http://122.xxx.xxx.xxx:8081" ] # 核心URL（抓包获取）          self . question_list_url  = "https://xxx.com/exam/question/bank" # 题库列表页          self . question_detail_url  = "https://xxx.com/question/detail" # 题目详情页 # 随机获取代理 def get_random_proxy ( self ) : return  random . choice ( self . proxy_pool ) if  self . proxy_pool  else None # 封装请求方法：添加延时、重试、代理 def send_request ( self ,  url ,  method = "GET" ,  params = None ,  data = None ) : # 随机延时1-3秒，模拟真人...
