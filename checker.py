import os
import requests

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 將你的粉專網址放進這裡
FACEBOOK_URLS = [
    "https://www.facebook.com/profile.php?id=61593044811347&locale=zh_TW", # Funbox 台中港3井
    "https://www.facebook.com/profile.php?id=100063893358626&locale=zh_TW", # Funbox 台中中友
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
    
    # 測試發送通知到 Discord（可以先用這行測試 Webhook 有沒有通）
    send_discord_alert("🤖 Funbox 抽獎通知機器人已成功啟動並連線！")

if __name__ == "__main__":
    main()
