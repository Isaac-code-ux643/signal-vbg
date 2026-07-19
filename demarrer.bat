@echo off
echo Demarrage du serveur et du tunnel...
echo.
cd /d "C:\Users\user\Documents\Default Project\signal_vbg"
start "Django Server" cmd /c "venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"
timeout /t 3 /nobreak >nul
echo Serveur demarre sur http://localhost:8000
echo.
echo Pour le lien public, ouvrez un terminal et tapez:
echo   ssh -R 80:localhost:8000 serveo.net
echo.
echo Ou telechargez cloudflared et tapez:
echo   cloudflared tunnel --url http://localhost:8000
echo.
pause
