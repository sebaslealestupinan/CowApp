@echo off
echo Deteniendo servidor actual...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>nul

echo.
echo Instalando dependencias...
pip install -q jinja2 python-multipart

echo.
echo Iniciando servidor...
uvicorn app.main:app --reload
