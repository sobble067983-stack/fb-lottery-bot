import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 設定你要追蹤的粉專網址
FACEBOOK_URLS = [
    ("Funbox 台中港3井", "https://m.facebook.com/profile.php?id=61593044811347"),
    ("Funbox 台中中友", "https://m.facebook.com/profile.php?id=100063893358626"),
]

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        print("未設定 Discord Webhook")
        return
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("成功發送到 Discord！")
    else:
        print(f"發送失敗: {response.text}")

def main():
    print("開始檢查各粉專最新動態...")
    
    # 放寬關鍵字清單（包含陀螺、抽獎等）
    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "BEYBLADE", "Funbox"]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (Mobile/15E148)"
    }

    found_count = 0

    for store_name, url in FACEBOOK_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"檢查 {store_name} - 狀態碼: {response.status_code}")
            
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            
            # 使用更通用的文章區塊抓取
            posts = soup.find_all("div", {"role": "article"})
            if not posts:
                # 備用抓取法
                posts = soup.find_all("div", {"data-ft": True})

            print(f"找到 {store_name} 的文章數量: {len(posts)}")

            for post in posts[:3]: # 檢查最新 3 篇
                text = post.get_text()
                
                # 檢查是否包含關鍵字
                if any(kw in text for kw in keywords):
                    found_count += 1
                    # 擷取部分內文避免過長
                    snippet = text[:150].replace("\n", " ")
                    alert_msg = f"🚨 **【{store_name} 發現相關貼文！】**\n> {snippet}...\n🔗 網址：{url}"
                    send_discord_alert(alert_msg)
                    print(f"已發送 {store_name} 的通知")
                    break # 每個粉專抓最新符合的一篇就好
                    
        except Exception as e:
            print(f"檢查 {store_name} 時發生錯誤: {e}")

    # 如果沒有抓到符合的貼文，也可以發送一個短訊息確認排程正常（選用）
    print(f"檢查結束，共發送 {found_count} 筆通知。")

if __name__ == "__main__":
    main()
