@echo off
echo Updating translation files...

REM Make message files
python manage.py makemessages -l ru
python manage.py makemessages -l kk

echo Translation files updated. Please edit the .po files in the locale directory.
echo After editing, run compile_translations.bat to compile the translations.
pause