import os
import requests
import feedparser

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 這次直接使用這兩個範例連結 (若這兩個沒資料，代表 RSS 來源網址需要更換)
FACEBOOK_FEEDS = [
    ("測試粉專", "https://rss.app/feeds/v1.1/user_100063893358626.json"), 
]

def send_discord_alert(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    for store_name, feed_url in FACEBOOK_FEEDS:
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            send_discord_alert(f"❌ 錯誤：無法從 {store_name} 獲取任何資料。")
            continue
            
        # 強制把前 3 篇標題印出來傳送到 Discord
        msg = f"🔍 **來自 {store_name} 的最新發現：**\n"
        for i, entry in enumerate(feed.entries[:3]):
            msg += f"{i+1}. {entry.title}\n"
        
        send_discord_alert(msg)
        print("已嘗試強制發送標題到 Discord")

if __name__ == "__main__":
    main()
