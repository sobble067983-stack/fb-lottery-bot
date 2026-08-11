import os
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 設定你要追蹤的粉專網址 (建議改用行動版 m.facebook.com 更好解析)
FACEBOOK_URLS = [
    ("Funbox 台中港3井", "https://m.facebook.com/profile.php?id=61593044811347"),
    ("Funbox 台中中友", "https://m.facebook.com/profile.php?id=100063893358626"),
]

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def main():
    print("開始檢查各粉專最新動態...")
    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "BEYBLADE"]
    
    # 模擬手機瀏覽器的標頭，避免被 Facebook 直接擋掉
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (Mobile/15E148)"
    }

    for store_name, url in FACEBOOK_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"無法讀取 {store_name} (狀態碼: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            
            # 抓取行動版網頁上的內文區塊
            posts = soup.find_all("div", {"data-ft": True})
            
            for post in posts[:3]: # 檢查最新 3 篇貼文
                text = post.get_text()
                
                # 檢查是否包含關鍵字
                if any(kw in text for kw in keywords):
                    # 避免重複通知，你可以加上簡單的過濾或直接發送
                    alert_msg = f"🚨 **【{store_name} 發現符合貼文！】**\n```{text[:200]}...```\n🔗 網址：{url}"
                    send_discord_alert(alert_msg)
                    print(f"已發送 {store_name} 的通知")
                    break # 找到最新的一篇就跳出
                    
        except Exception as e:
            print(f"檢查 {store_name} 時發生錯誤: {e}")

if __name__ == "__main__":
    main()
