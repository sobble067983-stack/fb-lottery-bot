import os
import requests
import feedparser  # 如果你需要用 RSS 輔助，或是直接用其他方式

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 放你的 30 家店網址或 RSS 來源
FACEBOOK_URLS = [
    "https://www.facebook.com/profile.php?id=100063893358626", # 玩具e哥 台中文心
    # ...其他店家
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
    keywords = ["抽獎", "line", "LINE", "方格"]
    
    # 這裡你可以加入你的抓取與比對邏輯
    # 當比對到符合 keywords 的貼文時，執行下面這行：
    # send_discord_alert("🚨 發現玩具e哥有新的抽獎貼文！\n連結：...")

if __name__ == "__main__":
    main()
