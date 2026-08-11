import os
import requests
import feedparser

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 使用公開且穩定的轉址來源來繞過 FB 的 IP 封鎖
# 這樣 GitHub 就能安全讀取到粉專的最新文章
FACEBOOK_FEEDS = [
    ("Funbox 台中港3井", "https://rss.app/feeds/v1.1/user_100063893358626.json"), # 透過安全通道轉譯
    ("Funbox 台中中友", "https://rss.app/feeds/v1.1/user_100063893358626.json"), # 可替換為對應的轉譯網址
]

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    print("開始透過安全通道檢查粉專動態...")
    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "BEYBLADE", "追蹤", "Funbox"]

    for store_name, feed_url in FACEBOOK_FEEDS:
        try:
            # 解析安全通道傳回的結構化資料
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                print(f"無法讀取 {store_name} 的資料")
                continue

            # 檢查最新的一篇貼文
            latest_entry = feed.entries[0]
            title = latest_entry.get("title", "")
            summary = latest_entry.get("summary", "")
            link = latest_entry.get("link", "")
            
            content = f"{title} {summary}"
            print(f"[{store_name}] 最新文章標題: {title}")

            # 檢查是否包含關鍵字
            if any(kw.lower() in content.lower() for kw in keywords):
                alert_msg = f"🚨 **【{store_name} 發現符合貼文！】**\n> {title}\n🔗 網址：{link}"
                send_discord_alert(alert_msg)
                print(f"已成功發送 {store_name} 的通知！")

        except Exception as e:
            print(f"檢查 {store_name} 時發生錯誤: {e}")

if __name__ == "__main__":
    main()
