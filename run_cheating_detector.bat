@echo off
echo Starting Cheating Detector...
cd /d "%~dp0"

REM Run detect.py in a new terminal
start cmd /k "cd cheating_detection_project && C:\Users\arpit\AppData\Local\Programs\Python\Python310\python.exe detect.py"

REM Run app.py (Flask) in another new terminal
start cmd /k "cd cheating_detection_project && C:\Users\arpit\AppData\Local\Programs\Python\Python310\python.exe app.py"

echo Done!
pause
