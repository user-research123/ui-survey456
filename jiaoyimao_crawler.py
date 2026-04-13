import requests
import json
import csv
import time
from datetime import datetime

def crawl_jiaoyimao_goods():
    """爬取交易猫商品数据"""
    url = "https://mtop.jiaoyimao.com/h5/mtop.com.jym.layout.pc.goodslist.getunifiedgoodslist/1.0/"
    
    all_goods = []
    page =1
    
    print(f"开始爬取交易猫商品数据...")
    
    while True:
        try:
            params = {
                'jsv': '2.6.2',
                'appKey': '12574478',
                't': str(int(time.time() *1000)),
                'sign': '557c39485d396612d6700531611359fd',
                'dataType': 'json',
                'valueType': 'original',
                'type': 'originaljson',
                'v': '1.0',
                'api': 'mtop.com.jym.layout.pc.goodslist.getUnifiedGoodsList',
                'ttid': 'jym_001@safari_pc_605.1.15_jiaoyimao',
                'preventFallback': 'true',
                'data': json.dumps({
                    "gameId":2007851,
                    "pageNo": page,
                    "pageSize":100,
                    "sortType": "default"
                })
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.jiaoyimao.com/jg2007851/?spm=gcmall.pc_home.0.0',
                'Accept': 'application/json, text/plain, */*',
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code ==200:
                result = response.json()
                
                if result.get('data', {}).get('data'):
                    goods_list = result['data']['data']
                    
                    if not goods_list:
                        print(f"第{page}页无数据,结束爬取")
                        break
                    
                    for goods in goods_list:
                        item = {
                            '商品ID': goods.get('id', ''),
                            '商品标题': goods.get('title', ''),
                            '价格': goods.get('price', ''),
                            '商品链接': f"https://www.jiaoyimao.com/jg2007851/{goods.get('id', '')}.html",
                            '卖家': goods.get('sellerNick', ''),
                            '保障服务': goods.get('guarantee', ''),
                            '想要人数': goods.get('wantBuyCount',0),
                            '服务器': goods.get('serverName', ''),
                            '账号类型': goods.get('accountType', ''),
                        }
                        all_goods.append(item)
                    
                    print(f"第{page}页获取到 {len(goods_list)}条数据,累计 {len(all_goods)}条")
                    
                    if len(goods_list)< 100:
                        print("已获取所有数据")
                        break
                    
                    page +=1
                    time.sleep(1)
                else:
                    print("无更多数据")
                    break
            else:
                print(f"请求失败,状态码: {response.status_code}")
                break
                
        except Exception as e:
            print(f"爬取第{page}页时出错: {e}")
            break
    
    return all_goods

def save_to_csv(goods_data, filename):
    """保存为CSV文件"""
    if not goods_data:
        print("无数据可保存")
        return
    
    if goods_data:
        fieldnames = list(goods_data[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(goods_data)
        
        print(f"数据已保存至: {filename}")
        print(f"共保存 {len(goods_data)}条商品数据")

if __name__ == '__main__':
    goods_data = crawl_jiaoyimao_goods()
    
    if goods_data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"jiaoyimao_goods_{timestamp}.csv"
        save_to_csv(goods_data, filename)
    else:
        print("未获取到商品数据")
