# Развертывание Expense Tracker на Google Cloud Platform

## Предварительные требования

1. Аккаунт Google Cloud Platform (GCP)
2. Установленный Google Cloud SDK (gcloud)
3. Созданный проект в Google Cloud
4. Включенный API App Engine
5. Созданный экземпляр Cloud SQL PostgreSQL

## Шаги по настройке базы данных

1. Создайте экземпляр Cloud SQL PostgreSQL:
   ```
   gcloud sql instances create expense-tracker-db --database-version=POSTGRES_13 --tier=db-f1-micro --region=YOUR-REGION
   ```

2. Создайте базу данных:
   ```
   gcloud sql databases create appdatabase1 --instance=expense-tracker-db
   ```

3. Создайте пользователя:
   ```
   gcloud sql users create admin123 --instance=expense-tracker-db --password=Qqwerty1!
   ```

## Настройка проекта

1. Откройте файл `app.yaml` и убедитесь, что переменные окружения настроены правильно.

2. Откройте файл `ExpenseTracker/settings.py` и замените строку:
   ```python
   'HOST': os.getenv('DB_HOST', '/cloudsql/YOUR-PROJECT-ID:YOUR-REGION:YOUR-INSTANCE-NAME'),
   ```
   на ваши реальные данные, например:
   ```python
   'HOST': os.getenv('DB_HOST', '/cloudsql/expense-tracker-123456:us-central1:expense-tracker-db'),
   ```

3. Откройте файл `deploy.bat` и замените `YOUR-PROJECT-ID` на ID вашего проекта в Google Cloud.

## Развертывание

1. Запустите скрипт `deploy.bat` для сбора статических файлов и деплоя на Google App Engine:
   ```
   deploy.bat
   ```

2. После успешного деплоя, выполните миграции базы данных:
   ```
   gcloud app instances ssh --service=default --version=[VERSION] -- python manage.py migrate
   ```
   где [VERSION] - версия вашего приложения (обычно 1).

3. Создайте суперпользователя (если нужно):
   ```
   gcloud app instances ssh --service=default --version=[VERSION] -- python manage.py createsuperuser
   ```

## Доступ к приложению

После успешного деплоя ваше приложение будет доступно по адресу:
```
https://[YOUR-PROJECT-ID].appspot.com
```

## Устранение неполадок

1. Проверьте логи приложения:
   ```
   gcloud app logs tail
   ```

2. Если возникают проблемы с базой данных, убедитесь, что:
   - Экземпляр Cloud SQL запущен
   - Ваше приложение имеет доступ к Cloud SQL
   - Настройки подключения в settings.py верны

3. Для проблем со статическими файлами:
   - Убедитесь, что вы выполнили `python manage.py collectstatic`
   - Проверьте, что в app.yaml правильно настроен обработчик для /static