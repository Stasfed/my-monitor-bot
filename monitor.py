import requests
from bs4 import BeautifulSoup
import hashlib
import os
import sys

URL = "https://cetatenie.just.ro/ordine-articolul-1-1/"
HASH_FILE = "last_hash.txt"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)

def get_page_content():
    try:
        response = requests.get(URL, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        send_telegram(f"❌ Ошибка при получении страницы: {e}")
        sys.exit(0)  # завершаем, но без ошибки для Actions

def main():
    new_content = get_page_content()
    new_hash = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hash = f.read().strip()
    else:
        old_hash = ""

    if new_hash != old_hash:
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        send_telegram("⚡ Изменения на сайте!")
    else:
        print("Изменений нет.")

if __name__ == "__main__":
    main()
