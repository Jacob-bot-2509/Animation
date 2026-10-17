@echo off
cd /d D:\Animation-Model-Training
"D:\Python Interpreter 3147\python.exe" tools\witness_consumer.py --config configs\witness_automation.local.json --execute --watch >> "D:\Animation-Model-Training\reviews\witness-automation\runtime\deploy-records\2026-10-17-watch-deploy\res-%1-stdout.txt" 2>> "D:\Animation-Model-Training\reviews\witness-automation\runtime\deploy-records\2026-10-17-watch-deploy\res-%1-stderr.txt"
echo %ERRORLEVEL% > "D:\Animation-Model-Training\reviews\witness-automation\runtime\deploy-records\2026-10-17-watch-deploy\res-%1-exit-code.txt"
