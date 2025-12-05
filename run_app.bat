@echo off
chcp 65001 >nul
title PhoBERT App Launcher
cls

echo ==================================================
echo   DANG KHOI DONG HE THONG (Vui long cho...)
echo ==================================================

cd /d "%~dp0"

:: 2. Kiểm tra xem thư mục venv có tồn tại không
if not exist "venv" (
    echo [LOI] Khong tim thay thu muc 'venv'!
    echo Ban hay chac chan rang file .bat nay nam canh thu muc 'venv'.
    echo.
    echo Giai phap: Chay lenh 'python -m venv venv' de tao moi truong.
    pause
    exit
)

echo Dang mo ung dung...
".\venv\Scripts\python.exe" -m streamlit run app.py

:: 4. Giữ màn hình không bị tắt nếu có lỗi
if %errorlevel% neq 0 (
    echo.
    echo [CO LOI xay ra] Chuong trinh da dung lai.
    echo Hay chup anh man hinh loi nay de sua.
)
pause