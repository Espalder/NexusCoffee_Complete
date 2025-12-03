@echo off
echo ============================================
echo INICIANDO - Nexus Coffee Sistema de Gestión
echo ============================================
echo.
echo Activando entorno virtual...
call .venv\Scripts\activate.bat
echo.
echo Iniciando aplicación...
python main_modular.py
echo.
echo La aplicación se ha cerrado.
echo Presiona cualquier tecla para salir...
pause > nul