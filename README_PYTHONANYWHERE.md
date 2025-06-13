# Развертывание ExpenseTracker на PythonAnywhere

PythonAnywhere предлагает бесплатный хостинг для Python-приложений, включая Django.

## Подготовка проекта

1. Убедитесь, что ваш проект находится в Git репозитории (GitHub, GitLab)
2. Обратите внимание, что на бесплатном плане PythonAnywhere вы можете использовать только SQLite, а не PostgreSQL

## Шаги для развертывания

1. Создайте аккаунт на [PythonAnywhere](https://www.pythonanywhere.com)
2. Откройте консоль Bash и клонируйте ваш репозиторий:
   ```bash
   git clone https://github.com/ваш_логин/ваш_репозиторий.git
   ```

3. Создайте виртуальное окружение и установите зависимости:
   ```bash
   cd ваш_репозиторий
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Измените настройки базы данных в `settings.py` для использования SQLite:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       }
   }
   ```

5. Выполните миграции и создайте суперпользователя:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Настройте веб-приложение в панели управления PythonAnywhere:
   - Перейдите на вкладку "Web"
   - Нажмите "Add a new web app"
   - Выберите "Manual configuration" и версию Python
   - Укажите путь к виртуальному окружению: `/home/ваш_логин/ваш_репозиторий/venv`
   - Настройте WSGI файл, указав путь к вашему приложению

7. Настройте статические файлы:
   - В разделе "Static files" добавьте:
     - URL: `/static/`
     - Directory: `/home/ваш_логин/ваш_репозиторий/static/`

8. Перезапустите веб-приложение

## Преимущества PythonAnywhere

- Простой процесс настройки
- Бесплатный SSL-сертификат
- Консоль для управления проектом
- Не "засыпает" как некоторые другие бесплатные хостинги

## Ограничения бесплатного плана PythonAnywhere

- Только SQLite (не PostgreSQL)
- Ограниченная вычислительная мощность
- Домен будет вида `ваш_логин.pythonanywhere.com`
- Ограничения на исходящий трафик (только определенные сайты доступны)