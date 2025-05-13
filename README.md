# Меню бот
Для развёртывания:
1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/Andrey-66/Menu_bot.git
   ```
   ```bash
   git clone https://github.com/ваш_репозиторий/Menu_bot.git
   ```
2. **Создание виртуального окружения**
   Для создания виртуального окружения выполните следующую команду:
   ```bash
   python -m venv venv
   ```
3. **Активация виртуального окружения**
   На Windows:
   ```bash
   venv\Scripts\activate
   ```
4. **Установка зависимостей**
   Установите необходимые зависимости, используя `pip`:
   ```bash
   pip install -r requirements.txt
   ```
5. **Настройка файла `.env`**  
   Создайте файл `.env` в корне проекта и добавьте следующую переменную окружения:
   ```plaintext
   TOKEN=ваш_токен_бота
   ```
6. **Создание файла `yabar-bot-2edc386bc135.json`**  
   Создайте файл `yabar-bot-2edc386bc135.json` в корне проекта и добавьте в него ключи от Google API.
7. **Настройка файла `constants.py`**  
   Откройте файл `constants.py` и добавьте необходимые константы для вашего проекта. Например:
   ```python
   GOOGLE_SCOPES = [
       "https://www.googleapis.com/auth/spreadsheets.readonly",
       "https://www.googleapis.com/auth/drive.readonly",
   ]
   GOOGLE_CREDENTIALS_FILE = "yabar-bot-2edc386bc135.json"
   SPREADSHEET_ID = "ваш_spreadsheet_id"
   SPREADSHEET_RANGE_RECIPES = "'Меню'!A2:C"
   SPREADSHEET_RANGE_INGREDIENTS = "'Ингредиенты'!A2:D"
   SPREADSHEET_RANGE_COCKTAILS = "'Настройки'!B2:B"
   SPREADSHEET_RANGE_AVAILABLE_COCKTAILS = "'Меню'!A2:A"
   MENU_TITLE = "📖 МЕНЮ:\n"
   COCKTAIL_SMILE = "🍹"
   MEDIA_DIR = "media"
   LOGGER_LEVEL = logging.INFO
   ```
8. **Настройка ключей для GitHub Actions**  
   Перейдите в настройки вашего репозитория на GitHub и добавьте следующие секреты:
   - `USER`: ваш пользователь для доступа к базе данных.
   - `PASSWORD`: ваш пароль для доступа к базе данных.
   - `HOST`: адрес вашего сервера базы данных.
