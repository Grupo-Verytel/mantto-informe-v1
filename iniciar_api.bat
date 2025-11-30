@echo off
echo ========================================
echo Iniciando API FastAPI
echo ========================================
echo.
echo URL: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause

