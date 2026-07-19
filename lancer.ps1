Write-Host "=== Signal VBG - Demarrage ===" -ForegroundColor Magenta
Write-Host ""

# Demarrer le serveur Django
Write-Host "Demarrage du serveur Django..." -ForegroundColor Yellow
$server = Start-Process -FilePath "C:\Users\user\Documents\Default Project\signal_vbg\venv\Scripts\python.exe" `
    -ArgumentList "manage.py runserver 0.0.0.0:8000" `
    -WorkingDirectory "C:\Users\user\Documents\Default Project\signal_vbg" `
    -PassThru

Start-Sleep -Seconds 3
Write-Host "Serveur Django demarre (PID: $($server.Id))" -ForegroundColor Green
Write-Host "  Local: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

# Demarrer le tunnel SSH via serveo
Write-Host "Demarrage du tunnel public..." -ForegroundColor Yellow
Write-Host "  En attente de l'URL publique..." -ForegroundColor Gray

# Lire la sortie du tunnel en temps reel
$tunnel = Start-Process -FilePath "ssh" `
    -ArgumentList "-o StrictHostKeyChecking=no -R 80:localhost:8000 serveo.net" `
    -NoNewWindow -PassThru

Start-Sleep -Seconds 8
Write-Host ""
Write-Host "Tunnel actif!" -ForegroundColor Green
Write-Host "  Ouvrez ce lien dans un navigateur:" -ForegroundColor Yellow
Write-Host "  https://serveo.net" -ForegroundColor White
Write-Host "  (le navigateur vous redirigera automatiquement)" -ForegroundColor Gray
Write-Host ""
Write-Host "Pour arreter: fermez cette fenetre" -ForegroundColor DarkGray

# Garder le script actif
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter..." -ForegroundColor DarkGray
try { $server.WaitForExit() } catch {}
