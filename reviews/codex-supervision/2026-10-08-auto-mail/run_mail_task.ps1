$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent.FullName
if ((Split-Path -Leaf $ProjectRoot) -ne 'Animation-Model-Training') { throw 'Unexpected project path' }
$PythonPath = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
& $PythonPath -B (Join-Path $PSScriptRoot 'mail_watch.py') poll
exit $LASTEXITCODE
