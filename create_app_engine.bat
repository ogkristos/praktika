@echo off
echo Создание App Engine для проекта...

REM Создаем App Engine в регионе europe-west3
gcloud app create --region=europe-west3

echo App Engine создан успешно.
pause