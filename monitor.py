import os
import requests
from bs4 import BeautifulSoup
import difflib

URL = "https://cetatenie.just.ro/ordine-articolul-1-1/"
CACHE_FILE = "last_content.html"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def get_page_content():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # можно ограничить часть страницы, например только контент статей
    return soup.get_text()

def main():
    new_content = get_page_content()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            old_content = f.read()
    else:
        old_content = ""

    if new_content != old_content:
        # сравнение строк и поиск отличий
        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            lineterm="",
        )
        diff_text = "\n".join(list(diff))

        if not diff_text.strip():
            diff_text = "Изменения есть, но не удалось вычислить разницу."

        # Telegram ограничивает сообщение 4096 символами
        if len(diff_text) > 4000:
            diff_text = diff_text[:4000] + "\n... (обрезано)"

        send_telegram_message(f"⚠️ Страница изменилась!\n\n<pre>{diff_text}</pre>")

        # обновляем кэш
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print("Нет изменений")

if __name__ == "__main__":
    main()
