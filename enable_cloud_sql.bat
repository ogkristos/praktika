@echo off
echo Настройка доступа Cloud SQL для App Engine...

REM Добавляем разрешение для App Engine подключаться к Cloud SQL
gcloud sql instances patch django-db-instance --authorized-networks=0.0.0.0/0

REM Добавляем сервисный аккаунт App Engine как пользователя Cloud SQL
gcloud projects add-iam-policy-binding expensetracker-462801 ^
  --member=serviceAccount:expensetracker-462801@appspot.gserviceaccount.com ^
  --role=roles/cloudsql.client

echo Настройка доступа завершена.
pause