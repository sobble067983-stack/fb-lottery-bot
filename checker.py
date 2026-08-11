import os
import requests
import feedparser

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 使用 RSSHub 的免費公共節點轉譯 FB 粉絲團
# 格式為: https://rsshub.app/facebook/page/粉專ID
PAGES = [
    ("Funbox 台中中友", "100063893358626"),
    ("Funbox 台中港3井", "61593044811347"),
]

def send_discord_alert(message):
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    print("開始監控粉絲團公告...")
    
    for name, page_id in PAGES:
        # 使用 RSSHub 免費節點
        url = f"https://rsshub.app/facebook/page/{page_id}"
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"無法取得 {name} 的資料")
            continue
            
        # 抓取最新一篇文章
        latest = feed.entries[0]
        title = latest.title
        link = latest.link
        
        # 為了避免重複發送，我們可以透過 GitHub Action 的 Cache 或簡單比較
        # 這裡先發送通知讓你測試
        alert_msg = f"📢 **【{name} 有新動態！】**\n標題：{title}\n🔗 請立即檢查 FB 或 LINE 記事本：{link}"
        send_discord_alert(alert_msg)
        print(f"已發送 {name} 的公告通知")

if __name__ == "__main__":
    main()
