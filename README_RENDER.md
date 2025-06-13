# Развертывание ExpenseTracker на Render.com

## Подготовка проекта

1. Убедитесь, что ваш проект находится в Git репозитории (GitHub, GitLab или Bitbucket)
2. Используйте файл `requirements_render.txt` вместо обычного `requirements.txt`
3. Используйте файл `render.yaml` для автоматической настройки сервисов

## Шаги для развертывания

1. Создайте аккаунт на [Render.com](https://render.com)
2. Подключите свой Git репозиторий
3. Создайте новый Web Service:
   - Выберите ваш репозиторий
   - Укажите имя сервиса (например, "expensetracker")
   - Выберите тип "Python"
   - Укажите команду сборки: `pip install -r requirements_render.txt`
   - Укажите команду запуска: `gunicorn ExpenseTracker.wsgi:application`
   - Добавьте переменную окружения `DJANGO_SETTINGS_MODULE=ExpenseTracker.settings_render`
   - Выберите бесплатный план

4. Создайте PostgreSQL базу данных:
   - В панели управления Render выберите "New" -> "PostgreSQL"
   - Укажите имя (например, "expensetracker-db")
   - Выберите бесплатный план
   - После создания базы данных, скопируйте строку подключения (Internal Database URL)

5. Добавьте строку подключения к базе данных в переменные окружения вашего Web Service:
   - Вернитесь к настройкам вашего Web Service
   - Добавьте переменную окружения `DATABASE_URL` со значением строки подключения

6. Запустите миграции базы данных:
   - В панели управления Web Service выберите "Shell"
   - Выполните команду: `python manage.py migrate`
   - Создайте суперпользователя: `python manage.py createsuperuser`

7. Ваше приложение будет доступно по URL вида: `https://expensetracker.onrender.com`

## Ограничения бесплатного плана Render

- Бесплатные веб-сервисы "засыпают" после 15 минут неактивности
- Бесплатные базы данных PostgreSQL имеют ограничение в 1 ГБ хранилища
- Бесплатные базы данных автоматически удаляются через 90 дней