@echo off
REM Launch a single ThreatChain node.
REM Usage: run_node.bat <node_name> <port> [peer_url]
REM Example: run_node.bat alice 5000
REM          run_node.bat bob   5001 http://127.0.0.1:5000

set NODE=%1
set PORT=%2
set PEER=%3
if "%NODE%"=="" set NODE=alice
if "%PORT%"=="" set PORT=5000

if "%PEER%"=="" (
  python app.py --node %NODE% --port %PORT%
) else (
  python app.py --node %NODE% --port %PORT% --peer %PEER%
)
