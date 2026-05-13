@echo off
REM Launch a 3-node ThreatChain demo network in separate windows.
REM Each node has its own data folder under prototype/data/<name>.

start "ThreatChain · alice" cmd /k python app.py --node alice --port 5000
timeout /t 2 /nobreak >nul

start "ThreatChain · bob"   cmd /k python app.py --node bob   --port 5001 --peer http://127.0.0.1:5000
timeout /t 2 /nobreak >nul

start "ThreatChain · carol" cmd /k python app.py --node carol --port 5002 --peer http://127.0.0.1:5000 --peer http://127.0.0.1:5001

echo.
echo Three nodes are starting:
echo   alice : http://127.0.0.1:5000
echo   bob   : http://127.0.0.1:5001
echo   carol : http://127.0.0.1:5002
echo.
