# PC端“<em>交易猫</em>”网站爬虫项目-CSDN博客

URL: https://m.blog.csdn.net/weixin_46332901/article/details/104885973

Query: 交易猫API接口 mtop.jiaoyimao.com商品列表获取方法

---

一、数据来源
数据来源于交易猫(jiaoyimao.com)。
交易猫(jiaoyimao.com)是国内专业的手机游戏交易平台,安全可靠的手游交易网站,提供手游账号交易、买号卖号、苹果代充值、游戏充值、首充号、装备道具、游戏币交易的手机网游交易平台。 打开交易猫网站首页，在搜索栏处，在“选择游戏”下拉选框处选择：王者荣耀；“商品类型”选择QQ账号；“区服”选择全部区服。
二、使用技术
Python语言
三、导入模块
requests模块 lxml模块 json模块 time模块 csv模块
四、代码
# -*- coding:utf-8 -*- import  requests  from  lxml  import  html  import  json  import  time  import  csv    def get_page ( url ,  verify = False ,  params = {         } ,  encoding = "utf8" ) :      headers  = {         "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" }      response  =  requests . get ( url ,  verify = verify ,  params = params ,  headers = headers )      response . encoding  =  encoding      return  response . text    def cun_json ( zong_list ) : with open ( "data.json" , "w" ,  encoding = "utf8" ) as  f :           json . dump ( zong_list ,  f ,  ensure_ascii = False ,  skipkeys = True ,  indent = 2 ) def cun_csv ( zong_list ) :      headers  = [ "商品" , "商品价格" , "投保情况" , "操作系统" , "所属游戏" , "绑定人脸" , "绑定至尊宝" , "角色等级" , "召唤师等级" , "贵族等级" , "段位" ,
