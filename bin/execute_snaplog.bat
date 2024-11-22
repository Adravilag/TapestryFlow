@echo off
@chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Establecer el directorio base del proyecto
SET BASE_DIR=%~dp0..

REM Activar el entorno virtual
CALL "%BASE_DIR%\tapestryflow_env\Scripts\activate.bat"

REM Ejecutar el script principal de SnapLog
python "%BASE_DIR%\snaplog\app\main.py"

REM Desactivar el entorno virtual
deactivate
