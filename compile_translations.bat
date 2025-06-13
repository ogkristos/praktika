@echo off
echo Compiling translation files...

REM Compile message files
python manage.py compilemessages

echo Translation files compiled successfully.
pause