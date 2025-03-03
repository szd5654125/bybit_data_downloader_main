import requests
import time
import random
from download_fundingrate import get_bybit_u_perp_symbols, download_file


symbols = get_bybit_u_perp_symbols()

# 目标 API 端点
url = "https://api2.bybit.com/contract/v5/support/funding-rate-list-export?symbol=BTCUSDT"

# 构造 Headers（从开发者工具中复制关键的请求头）
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,de;q=0.8,en;q=0.7,zh-TW;q=0.6",
    "origin": "https://www.bybit.com",
    "referer": "https://www.bybit.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 "
                  "Safari/537.36"
}

for symbol in symbols:
    print(f"正在请求 {symbol} 的资金费率历史...")

    url = f"https://api2.bybit.com/contract/v5/support/funding-rate-list-export?symbol={symbol}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "result" in data and "downloadUrl" in data["result"]:
            download_url = data["result"]["downloadUrl"]
            print(f"{symbol} 下载链接: {download_url}")

            # 下载 Excel 文件
            download_file(download_url, f"{symbol}_funding_rate.xlsx")
        else:
            print(f"❌ {symbol} 的 API 响应格式不正确")
    else:
        print(f"❌ {symbol} 请求失败，状态码: {response.status_code}")
    # 添加 1-3 秒的随机暂停
    sleep_time = random.uniform(1, 3)
    print(f"随机等待 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)
print("所有资金费率数据下载完成！")