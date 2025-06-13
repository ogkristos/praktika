@echo off
echo Deploying to Google Cloud Platform...

REM Collect static files
python manage.py collectstatic --noinput

REM Deploy to Google App Engine
gcloud app deploy app.yaml --project expensetracker-462801

echo Deployment completed.
pause