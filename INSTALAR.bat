@echo off
echo ============================================
echo INSTALADOR - Nexus Coffee Sistema de Gestión
echo ============================================
echo.
echo Creando entorno virtual...
python -m venv .venv
echo.
echo Activando entorno virtual...
call .venv\Scripts\activate.bat
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Instalación completada!
echo.
echo Para ejecutar el sistema, usa: EJECUTAR.bat
echo Presiona cualquier tecla para salir...
pause > nul