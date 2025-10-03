import requests
from bs4 import BeautifulSoup
import hashlib
import os
import sys
import difflib

URL = "https://cetatenie.just.ro/ordine-articolul-1-1/"
HASH_FILE = "last_hash.txt"
CONTENT_FILE = "last_content.txt"
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
        sys.exit(0)


def main():
    new_content = get_page_content()
    new_hash = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

    old_hash = ""
    old_content = ""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hash = f.read().strip()
    if os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            old_content = f.read()

    if new_hash != old_hash:
        # сохраняем новые данные
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        if old_content:
            # формируем diff
            diff = difflib.unified_diff(
                old_content.splitlines(),
                new_content.splitlines(),
                lineterm="",
            )
            diff_text = "\n".join(diff)

            # телеграм не любит слишком длинные сообщения
            if len(diff_text) > 3500:
                diff_text = diff_text[:3500] + "\n...diff truncated..."

            send_telegram(f"⚡ Изменения на сайте!\n\n{diff_text}")
        else:
            send_telegram("⚡ Первое сохранение страницы.")
    else:
        print("Изменений нет.")


if __name__ == "__main__":
    main()
