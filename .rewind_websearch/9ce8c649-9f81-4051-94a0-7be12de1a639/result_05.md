# Streamlit基础入门与快速原型开发-CSDN技术社区

URL: https://m.blog.csdn.net/lisiyuan007/article/details/159881473

Query: fungjiewen-collab.github.io wangzhe_report index_with_tabs.html

---

引言：为什么选择 Streamlit ？
在当今数据驱动的世界中，快速构建交互式数据应用已成为 数据科学 家、分析师和开发者的核心需求。传统的Web开发流程（前端HTML/CSS/JavaScript + 后端Python/Node.js + 数据库 + API）虽然功能强大，但对于数据科学项目来说往往过于繁琐。这就是Streamlit诞生的背景。
Streamlit是一个开源的 Python 库，它允许您用纯Python代码快速创建自定义的Web应用。自2019年发布以来，它已经彻底改变了数据科学家分享其工作的方式。让我们通过以下对比来理解Streamlit的独特价值：
1. Streamlit核心概念解析
1.1 Streamlit的设计哲学
Streamlit的设计理念是"为数据科学而生的最快方式"。它基于以下几个核心原则：
拥抱Python ：所有功能都通过Python API暴露
即时反馈 ：每次交互都会重新运行脚本
简单至上 ：API设计直观，学习曲线平缓
开源免费 ：MIT许可证，社区驱动
1.2 Streamlit的架构模型
理解Streamlit的架构对于高效使用它至关重要：
这种独特的执行模型意味着： 每次用户交互都会导致整个脚本重新执行 。这看起来可能效率低下，但实际上通过智能的缓存机制，Streamlit能够高效地处理这种模式。
1.3 安装与环境配置
在开始第一个Demo之前，让我们确保环境正确配置。下面是推荐的设置方式：
# 环境配置检查脚本
# 文件名: check_environment.py
import  sys
import  subprocess
import  pkg_resources
def check_environment ():
"""检查Python环境和Streamlit安装"""
print ( "="  *  50 )
print ( "环境检查开始" )
print ( "="  *  50 )
# 检查Python版本
    python_version = sys.version_info
print ( f"Python版本:  {python_version.major} . {python_version.minor} . {python_version.micro} " )
if  python_version.major <  3 or  (python_version.major ==  3 and  python_version.minor <  8 ):
print ( "❌ 需要Python 3.8或更高版本" )
return False
print ( "✅ Python版本符合要求" )
# 检查必要包
    required_packages = [ 'streamlit' ,  'pandas' ,  'numpy' ,  'plotly' ]
for  package  in  required_packages:
try :
            version = pkg_resources.get_distribution(package).version
print ( f"✅  {package} :  {version} " )
except  pkg_resources.DistributionNotFound:
print ( f"❌  {package} : 未安装" )
print ( "="  *  50 )
print ( "要安装缺失的包，请运行:" )
print ( "pip install streamlit pandas numpy plotly matplotlib seaborn" )
print ( "="  *  50 )
return True
if  __name__ ==  "__main__" :
    check_environment()
一键获取完整项目代码 python
2. Demo 1: Streamlit最简示例
让我们从最简单的Streamlit应用开始，了解其基本结构。
# demo_hello_world.py
"""
Streamlit最简示例 - 演示基础功能
运行方式: streamlit run demo_hello_world.py
功能特点:
1. 展示Streamlit的核心UI组件
2. 演示交互式控件
3. 展示数据可视化
4. 演示布局系统
"""
import  streamlit  as  st
import  pandas  as  pd
import  numpy  as  np
import  time
from  datetime  import  datetime
# ============================
# 1. 页面配置
# ============================
st.set_page_config(
    page_title= "Streamlit快速入门演示" ,
    page_icon= "    " ,
    layout= "wide" ,   # 可选 "centered" 或 "wide"
    initial_sidebar_state= "expanded" # 可选 "auto", "expanded", "collapsed"
)
# ============================
# 2. 应用标题和介绍
# ============================
st.title( "     Streamlit快速入门" )
st.markdown( """
欢迎来到Streamlit世界！这是一个完整的入门示例，展示了Streamlit的核心功能。
从简单的文本展示到复杂的数据可视化，您将在这里找到一切。
""" )
# 添加一些装饰
st.divider()
# ============================
# 3. 侧边栏 - 控制面板
# ============================
with  st.sidebar:
    st.header( "⚙️ 控制面板" )
# 主题选择
    theme = st.selectbox(
"选择主题" ,
        [ "Light" ,  "Dark" ,  "Auto" ],
help = "选择应用的主题样式"
    )
# 更新频率
    update_freq = st.slider(
"数据更新频率(秒)" ,
        min_value= 1 ,
        max_value= 60 ,
        value= 10 ,
help = "控制数据自动更新的频率"
    )
# 功能开关
    st.subheader( "功能开关" )
    show_data = st.checkbox( "显示示例数据" , value= True )
    show_...
