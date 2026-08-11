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
    # 模擬更真實的手機瀏覽器標頭
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    keywords = ["抽獎", "line", "LINE", "方格", "陀螺", "beyblade", "BEYBLADE", "追蹤", "Funbox"]

    for store_name, url in FACEBOOK_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 把網頁裡所有 span 和 div 的文字全部抓出來組合成大字串
            all_text = ""
            for tag in soup.find_all(["span", "div", "p"]):
                all_text += tag.get_text() + "\n"

            # 為了讓你能在 GitHub Actions 的日誌中看看到底抓到了什麼，我們把它印出來
            print(f"[{store_name}] 抓到的總字數: {len(all_text)}")
            
            # 如果抓到的字數太少（小於 500 字），代表被 FB 擋掉或沒載入成功
            if len(all_text) < 500:
                print(f"警告：{store_name} 可能被 Facebook 阻擋，內容過少！")
                # 為了測試，強制發送一則通知告訴你它有在跑
                send_discord_alert(f"⚠️ 偵測通知：{store_name} 頁面遭到 FB 攔截或未載入內文。")
                continue

            # 檢查是否包含關鍵字
            found = False
            for kw in keywords:
                if kw in all_text:
                    found = True
                    break

            if found:
                alert_msg = f"🚨 **【{store_name} 發現符合關鍵字的貼文！】**\n🔗 網址：{url}"
                send_discord_alert(alert_msg)
                print(f"已成功發送 {store_name} 的通知！")
            else:
                print(f"{store_name} 內容中未發現指定關鍵字。")

        except Exception as e:
            print(f"錯誤: {e}")

if __name__ == "__main__":
    main()
