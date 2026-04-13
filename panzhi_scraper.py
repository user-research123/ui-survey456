import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv
import ssl
import os

# 临时禁用 SSL 验证以解决 Python 3.14 的证书问题
ssl._create_default_https_context = ssl._create_unverified_context

def start_scraper():
    # 1. 初始化浏览器 (启用伪装模式)
    options = uc.ChromeOptions()
    
    # 显式设置 Chrome 浏览器路径 (macOS 用户 jiewen 的桌面路径)
    chrome_path = "/Users/jiewen/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(chrome_path):
        options.binary_location = chrome_path
    else:
        print(f"警告: 未在标准路径找到 Chrome: {chrome_path}")
        print("请确保已安装 Google Chrome 浏览器。")
        return

    # 添加网络相关参数以解决 DNS 解析问题
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--no-proxy-server")

    driver = uc.Chrome(options=options)
    
    try:
        print("正在打开盼之代售网...")
        driver.get("https://www.pzds.com/game/wangzhe/")
        
        # 2. 关键：留出足够时间让您手动通过验证和登录
        print("="*50)
        print("请在浏览器中手动完成验证/登录。")
        print("完成后，回到终端按【回车键】继续爬取...")
        print("="*50)
        input() # 等待用户按回车
        
        # 3. 滚动页面加载更多内容 (可选，根据需求调整次数)
        print("正在加载页面数据...")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
        # 4. 提取数据 (注意：类名可能需要根据实际网页调整)
        # 这里使用通用的选择器尝试获取，如果获取不到，需要您提供具体的 HTML 结构
        items = driver.find_elements(By.CSS_SELECTOR, ".goods-list .goods-item") # 示例选择器，需确认
        
        data_list = []
        if not items:
            print("未找到商品元素，请检查 CSS 选择器是否正确。")
            print("提示：请按 F12 查看商品卡片的 class 名称，并修改脚本中的 selector。")
        else:
            print(f"找到 {len(items)} 个商品，开始提取...")
            for item in items:
                try:
                    # 以下选择器仅为示例，请务必根据实际网页结构调整
                    title_elem = item.find_element(By.CSS_SELECTOR, ".goods-title") 
                    price_elem = item.find_element(By.CSS_SELECTOR, ".goods-price")
                    
                    title = title_elem.text if title_elem else "未知标题"
                    price = price_elem.text if price_elem else "未知价格"
                    
                    data_list.append({
                        "标题": title,
                        "价格": price
                    })
                except Exception as e:
                    continue
                    
        # 5. 保存数据
        if data_list:
            df = pd.DataFrame(data_list)
            filename = "panzhi_wangzhe_data.csv"
            # 添加 BOM 头防止 Excel 乱码
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"成功！数据已保存至 {filename}")
            print(df.head())
        else:
            print("未能提取到有效数据。")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_scraper()