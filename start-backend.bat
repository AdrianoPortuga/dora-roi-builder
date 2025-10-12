@echo off
setlocal
cd /d C:\dora-roi-builder
call .venv\Scripts\activate
if not exist app\__init__.py type nul > app\__init__.py
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
endlocal
