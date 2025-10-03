import requests
import hashlib
import os

URL = "https://cetatenie.just.ro/ordine-articolul-1-1/"
HASH_FILE = "page_hash.txt"

# токен и chat_id из GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Нет TELEGRAM_TOKEN или CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload)
        if r.status_code != 200:
            print("Ошибка Telegram:", r.text)
    except Exception as e:
        print("Ошибка при отправке:", e)

def get_page_hash(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return hashlib.md5(response.text.encode("utf-8")).hexdigest()
    except Exception as e:
        print("Ошибка при загрузке:", e)
        return None

def load_old_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

def save_new_hash(new_hash):
    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

def main():
    print("🔍 Проверка страницы...")
    old_hash = load_old_hash()
    new_hash = get_page_hash(URL)
    if not new_hash:
        return
    if old_hash is None:
        print("Первый запуск — сохраняем хэш")
        save_new_hash(new_hash)
    elif old_hash != new_hash:
        print("⚠️ Страница изменилась!")
        send_telegram(f"⚠️ Страница изменилась!\n{URL}")
        save_new_hash(new_hash)
    else:
        print("Изменений нет.")

if __name__ == "__main__":
    main()
