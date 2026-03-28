@echo off
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pause
