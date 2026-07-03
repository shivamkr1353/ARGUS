@echo off
echo Starting ARGUS System...

:: Navigate to the project directory (optional if you run it directly from the folder, but safe)
cd /d "%~dp0"

:: Run the Streamlit app using the virtual environment explicitly if it exists
if exist "venv\Scripts\python.exe" (
    echo Virtual environment found. Launching Streamlit...
    venv\Scripts\python.exe -m streamlit run main.py
) else (
    echo No virtual environment found. Running with global Python...
    python -m streamlit run main.py
)

pause
