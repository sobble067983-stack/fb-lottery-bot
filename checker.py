import os
import requests

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def main():
    if DISCORD_WEBHOOK_URL:
        data = {"content": "🚨 強制測試：機器人有收到指令，正在連線！"}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"發送狀態碼: {response.status_code}")

if __name__ == "__main__":
    main()
