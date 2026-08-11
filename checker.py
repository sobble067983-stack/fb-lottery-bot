import os
import requests
from facebook_scraper import get_posts

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 直接填入粉專的名稱或 ID
# facebook-scraper 可以直接抓取公開粉專
FACEBOOK_PAGES = [
    ("Funbox 台中港3井", "61593044811347"),
    ("Funbox 台中中友", "100063893358626"),
]

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    print("開始使用開源套件抓取 FB 粉專...")
    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "BEYBLADE", "追蹤", "Funbox"]

    for store_name, page_id in FACEBOOK_PAGES:
        try:
            # 抓取該粉專最近的 3 篇貼文（完全免費）
            posts = get_posts(page_id, pages=1, timeout=10)
            
            for post in posts:
                text = post.get("text", "")
                post_url = post.get("post_url", "")
                
                print(f"[{store_name}] 抓到貼文預覽: {text[:50]}...")

                # 檢查關鍵字
                if any(kw.lower() in text.lower() for kw in keywords):
                    alert_msg = f"🚨 **【{store_name} 發現符合貼文！】**\n> {text[:150]}...\n🔗 網址：{post_url}"
                    send_discord_alert(alert_msg)
                    print(f"已發送 {store_name} 的通知！")
                    break # 只抓最新符合的一篇
                    
        except Exception as e:
            print(f"抓取 {store_name} 失敗: {e}")

if __name__ == "__main__":
    main()
