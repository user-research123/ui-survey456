# <em>阿里云函数计算</em> <em>FC</em> 实战：<em>部署</em> <em>Python</em> 爬虫服务并解决定时触发（Cron）延迟问题-CSDN博客

URL: https://m.blog.csdn.net/2501_93877712/article/details/154138517

Query: 阿里云函数计算 FC 部署 Python Flask 教程 2025 2026

---

一、环境准备
开通服务
登录阿里云控制台，开通「函数计算 FC」和「日志服务 SLS」（用于查看函数日志）。 安装阿里云 CLI 或使用控制台操作，推荐本地安装  funcraft  工具（FC 部署工具）： 
bash
npm install  @alicloud / fun  -g
AI写代码
本地项目结构 创建如下目录结构，用于存放爬虫代码和配置：
plaintext
spider-service/
├── index.py        # 爬虫主逻辑
├── requirements.txt   # 依赖库
└── template.yml    # FC 配置文件
AI写代码
二、编写  Python 爬虫 代码
以爬取示例网页数据为例， index.py  代码如下：
python
运行
import  requests
import  logging
# 配置日志（对接 SLS）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def handler ( event, context ):
"""FC 入口函数"""
try :
# 爬虫逻辑
        url =  "https://example.com"
        response = requests.get(url, timeout= 10 )
        logger.info( f"爬取成功，状态码： {response.status_code} " )
return  { "status" :  "success" ,  "data" : response.text[: 100 ]}   # 返回部分数据
except  Exception  as  e:
        logger.error( f"爬取失败： { str (e)} " )
return  { "status" :  "error" ,  "message" :  str (e)}
AI写代码
requirements.txt  声明依赖：
plaintext
requests = = 2.31.0
AI写代码
三、配置函数计算（template.yml）
通过  template.yml  定义 FC 函数、 触发器 和资源配置：
yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform :  'Aliyun::Serverless-2018-04-03'
Resources :
spider-service :  # 服务名
Type :  'Aliyun::Serverless::Service'
Properties :
Description :  'Python 爬虫服务'
LogConfig :  # 日志配置（需先创建 SLS 项目）
Project :  'fc-spider-log'   # SLS 项目名
Logstore :  'spider-logstore'   # SLS 日志库名
spider-function :  # 函数名
Type :  'Aliyun::Serverless::Function'
Properties :
Handler : index.handler  # 入口：文件名.函数名
Runtime : python3. 9   # 运行时环境
CodeUri : ./  # 代码目录
MemorySize :  256   # 内存配置（根据爬虫需求调整）
Timeout :  60   # 超时时间（单位：秒，爬虫耗时不宜过长）
Events :
cron-trigger :  # 定时触发器
Type : Timer
Properties :
Payload :  '{"trigger": "cron"}'   # 触发携带的参数
CronExpression :  '0 0 * * * *'   # Cron 表达式（UTC 时间，每天  0  点触发）
Enable : true  # 启用触发器
AI写代码
四、部署函数到阿里云 FC
初始化配置 执行  fun config  输入阿里云 AccessKey（需具备 FC 操作权限）。
部署函数 在项目根目录执行：
bash
fun  deploy -y
AI写代码
部署成功后，可在阿里云 FC 控制台查看函数和触发器。
五、解决定时触发（Cron）延迟问题
FC 定时触发器基于 Cron 表达式执行，但可能因资源调度等原因出现延迟。以下是优化方案：
1. 调整 Cron 表达式时区
FC 定时触发器默认使用  UTC 时间 ，若需按北京时间触发，需转换时区（北京时间 = UTC + 8）。例如：北京时间每天 8 点触发，对应 UTC 时间为 0 点，Cron 表达式为  0 0 * * * * 。
2. 优化函数资源配置
内存与超时时间 ：若爬虫处理数据量大，适当提高  MemorySize （如 512MB）和  Timeout ，避免因资源不足导致触发延迟。 预留实例 ：对于高频或严格定时需求，配置「预留实例」（在函数配置中开启），避免冷启动耗时。
3. 触发时间 精度 优化
FC 定时触发器的精度为  ±1 分钟 ，若需更高精度（如秒级），可在函数内添加「二次校准」逻辑： 
python
运行
import  time
def handler(event, context):
    target_ time = "08:00:00"   # 目标触发时间（北京时间）
    current_ time = time .strftime( "%H:%M:%S" ,  time .localtime())
if  current_ time >  target_ time :
        delay  =  (int(current_ time .split( ':' )[ 0 ]) * 3600 +  int(current_ time .split( ':' )[ 1 ]) * 60 +  int(current_ time .split( ':' )[ 2 ]))  -  \
                (int(target_ time .split( ':' )[ 0 ]) * 3600 +  int(target_ time .split( ':' )[ 1 ]) * 60 +  int(target_ time .split( ':' )[ 2 ]))
        logger.warning(f "触发延迟 {delay} 秒，跳过本次执行" )
return  { "status" :  "delayed" ,  "delay_seconds" : delay}
    # 正常爬虫逻辑...
AI写代码
4. 监控与告警
通过「云监控」配置触发器执行状态告警（如触发失败、延迟超过 5 分钟），及时发现问题。 查看 ...
