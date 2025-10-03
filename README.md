# Website Monitor Bot

Этот проект отслеживает изменения на странице:  
👉 [https://cetatenie.just.ro/ordine-articolul-1-1/](https://cetatenie.just.ro/ordine-articolul-1-1/)

Если страница изменилась — бот отправляет уведомление в **Telegram**.

## ⚙️ Как запустить

1. Создайте новый репозиторий на GitHub.
2. Загрузите в него файлы из этого проекта.
3. Перейдите в **Settings → Secrets and variables → Actions**.
4. Добавьте секреты:
   - `TELEGRAM_TOKEN` — токен вашего бота от BotFather
   - `CHAT_ID` — ваш chat_id
5. Вкладка **Actions** → убедитесь, что workflow активен.
6. Скрипт будет проверять сайт каждые 30 минут.
