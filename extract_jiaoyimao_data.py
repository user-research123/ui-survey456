import json
import re
from datetime import datetime

#从浏览器观察结果中提取的商品数据
goods_data = [
    {
        "title": "赠永久包赔六位uid6777446位ID号未开通安卓服务器微信账号-担保",
        "price": "¥150,000",
        "url": "https://www.jiaoyimao.com/jg2007851/1773828122501318.html?isGray=true"
    },
    {
        "title": "赠永久包赔极品ID号6位ID号未开通安卓服务器 QQ账号",
        "price": "¥10,000",
        "url": "https://www.jiaoyimao.com/jg2007851/1773740025086102.html?isGray=true"
    },
    {
        "title": "赠永久包赔看我的号码岚鸟印象异色-双灯鱼异色-月牙雪熊安卓服务器 QQ账号",
        "price": "¥999,999",
        "url": "https://www.jiaoyimao.com/jg2007851/1773798963596649.html?isGray=true"
    },
    {
        "title": "赠永久包赔7865246位ID号未开通安卓服务器 QQ账号",
        "price": "¥786,524",
        "url": "https://www.jiaoyimao.com/jg2007851/1773737853431431.html?isGray=true"
    },
    {
        "title": "赠永久包赔洛克极品靓号7位ID号未开通安卓服务器 QQ账号",
        "price": "¥500,000",
        "url": "https://www.jiaoyimao.com/jg2007851/1773745087135538.html?isGray=true"
    }
]

def save_to_csv(data, filename):
    """保存为CSV文件"""
    if not data:
        print("无数据可保存")
        return
    
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write("序号,商品标题,价格,商品链接\n")
        for i, item in enumerate(data,1):
            title = item['title'].replace(',', '，')
            price = item['price']
            url = item['url']
            f.write(f"{i},{title},{price},{url}\n")
    
    print(f"数据已保存至: {filename}")
    print(f"共保存 {len(data)}条商品数据")

if __name__ == '__main__':
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"jiaoyimao_goods_{timestamp}.csv"
    save_to_csv(goods_data, filename)
