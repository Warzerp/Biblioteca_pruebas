@echo off
setlocal
cd /d "%~dp0\.."
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
)
python database\crear_db.py
if errorlevel 1 exit /b 1
python manage.py migrate
if errorlevel 1 exit /b 1
python database\seed.py --reset
if errorlevel 1 exit /b 1
echo.
echo Base lista. Cuentas de prueba: database\CUENTAS_PRUEBA.md
endlocal
