@echo off
@chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Establecer el directorio base del proyecto
SET BASE_DIR=%~dp0..

REM Activar el entorno virtual
CALL "%BASE_DIR%\tapestryflow_env\Scripts\activate.bat"

REM Configurar PYTHONPATH para que incluya el directorio flowtools
SET PYTHONPATH=%BASE_DIR%\flowtools

REM Ejecutar el script principal de FlowTools
python "%BASE_DIR%\flowtools\app\main.py"

REM Desactivar el entorno virtual
deactivate
