import os
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

FACEBOOK_URLS = [
    ("Funbox 台中港3井", "https://m.facebook.com/profile.php?id=61593044811347"),
    ("Funbox 台中中友", "https://m.facebook.com/profile.php?id=100063893358626"),
]

def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "追蹤"]

    for store_name, url in FACEBOOK_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 抓取所有可能包含文字的區塊
            paragraphs = soup.find_all("p")
            all_text = " ".join([p.get_text() for p in paragraphs])
            
            print(f"[{store_name}] 抓到的文字內容預覽: {all_text[:300]}")

            # 只要抓到的文字包含關鍵字，就發送通知
            if any(kw.lower() in all_text.lower() for kw in keywords):
                alert_msg = f"🚨 **【{store_name} 發現新動態！】**\n內容包含關鍵字！\n🔗 網址：{url}"
                send_discord_alert(alert_msg)
                print(f"已發送 {store_name} 的通知")

        except Exception as e:
            print(f"錯誤: {e}")

if __name__ == "__main__":
    main()
