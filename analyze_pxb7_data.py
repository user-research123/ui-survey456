import json
import sys
from collections import Counter

def analyze_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    if not products:
        print("No products found.")
        return

    # 1. 价格分布
    prices = [p['price'] for p in products if p['price'] > 0]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        median_price = sorted(prices)[len(prices) // 2]
        
        # 区间分布
        ranges = {"0-500": 0, "500-1000": 0, "1000-5000": 0, "5000+": 0}
        for p in prices:
            if p <= 500:
                ranges["0-500"] += 1
            elif p <= 1000:
                ranges["500-1000"] += 1
            elif p <= 5000:
                ranges["1000-5000"] += 1
            else:
                ranges["5000+"] += 1
        
        price_dist = {k: f"{v/len(prices)*100:.1f}%" for k, v in ranges.items()}
    else:
        min_price = max_price = avg_price = median_price = 0
        price_dist = {}

    # 2. 平台占比
    platforms = [p['platform'] for p in products]
    platform_counts = Counter(platforms)
    total_platforms = sum(platform_counts.values())
    platform_ratio = {k: f"{v/total_platforms*100:.1f}%" for k, v in platform_counts.items()}

    # 3. ID特征 (由于提取的标题比较通用，这里暂时无法准确分析ID命名特征，将在报告中说明)
    id_features = "数据提取中未包含详细的ID命名信息，需进一步解析商品详情页。"

    summary = {
        "date": "2026-04-12",
        "total_products": len(products),
        "price_analysis": {
            "min": min_price,
            "max": max_price,
            "avg": round(avg_price, 2),
            "median": median_price,
            "distribution": price_dist
        },
        "platform_ratio": platform_ratio,
        "id_features": id_features
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Analysis saved to {output_file}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    input_json = "pxb7_products_20260412.json"
    output_json = "pxb7_analysis_20260412.json"
    analyze_data(input_json, output_json)
