@echo off
setlocal

set "PROJECT_DIR=C:\Users\suzan\Downloads\MOP"
set "SCRIPT=%PROJECT_DIR%\scripts\load_to_postgres.py"
set "LOG_DIR=%PROJECT_DIR%\logs"
set "LOG_FILE=%LOG_DIR%\weekly_postgres_refresh.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo.>> "%LOG_FILE%"
echo ==================================================>> "%LOG_FILE%"
echo Refresh started: %DATE% %TIME%>> "%LOG_FILE%"

if exist "%USERPROFILE%\anaconda3\python.exe" (
    set "PYTHON=%USERPROFILE%\anaconda3\python.exe"
) else if exist "%USERPROFILE%\miniconda3\python.exe" (
    set "PYTHON=%USERPROFILE%\miniconda3\python.exe"
) else (
    set "PYTHON=python"
)

cd /d "%PROJECT_DIR%"

"%PYTHON%" "%SCRIPT%" >> "%LOG_FILE%" 2>&1
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
    echo Refresh completed successfully: %DATE% %TIME%>> "%LOG_FILE%"
) else (
    echo Refresh FAILED with exit code %EXIT_CODE%: %DATE% %TIME%>> "%LOG_FILE%"
)

exit /b %EXIT_CODE%
