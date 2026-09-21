@echo off
title Customer Behavior Dashboard - Localhost Server
color 0B
cls
echo ==============================================================================
echo       CUSTOMER SHOPPING BEHAVIOR ANALYSIS - INTERACTIVE DASHBOARD
echo ==============================================================================
echo.
echo [1/3] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not detected in your PATH! Please install Python 3.9+.
    pause
    exit /b
)
python --version

echo.
echo [2/3] Checking dataset and database...
if not exist "cleaned_customer_shopping_behavior.csv" (
    echo Running ETL pipeline to clean data and initialize SQLite database...
    python data_pipeline.py
) else (
    echo Dataset and SQLite database are ready!
)

echo.
echo [3/3] Launching Localhost Dashboard on http://localhost:8501 ...
echo Opening your web browser automatically...
start http://localhost:8501

echo.
echo ==============================================================================
echo  DASHBOARD IS NOW RUNNING AT: http://localhost:8501
echo  Press Ctrl + C in this terminal window anytime to stop the server.
echo ==============================================================================
echo.

python -m streamlit run dashboard.py --server.port 8501 --server.headless true

pause
