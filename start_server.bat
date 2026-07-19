@echo off
cd /d "C:\Users\user\Documents\Default Project\signal_vbg"
call venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8000
