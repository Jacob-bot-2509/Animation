param([switch]$Execute, [switch]$SelfTest, [string]$Bind, [string]$Round,
      [string]$Exe = (Join-Path $PSScriptRoot 'witness_receiver_v3.exe'),
      [string]$OutputRoot = (Join-Path $PSScriptRoot 'captures'))
$ErrorActionPreference = 'Stop'
$expectedExe = '02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf'
if (-not $Execute) { Write-Output 'PLAN: no process started; choose -Execute with -Bind or -SelfTest'; exit 3 }
if ($SelfTest -and $Bind) { throw 'SelfTest and Bind are mutually exclusive' }
if (-not $SelfTest) {
    $ip = [System.Net.IPAddress]::Parse($Bind)
    if ($ip.Equals([System.Net.IPAddress]::Any) -or $ip.Equals([System.Net.IPAddress]::IPv6Any) -or
        [System.Net.IPAddress]::IsLoopback($ip) -or $ip.IsIPv6Multicast -or $ip.IsIPv6LinkLocal -or
        ($ip.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork -and
         (($ip.GetAddressBytes()[0] -ge 224) -or ($ip.GetAddressBytes()[0] -eq 169 -and $ip.GetAddressBytes()[1] -eq 254)))) {
        throw 'A specific witness unicast address is required'
    }
    $Bind = $ip.ToString()
}
if (-not $Round) { $Round = 'witness-' + [guid]::NewGuid().ToString('N') }
if ($Round -notmatch '^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$') { throw 'Invalid round identifier' }
$exePath = (Resolve-Path -LiteralPath $Exe).Path
$exeBefore = (Get-FileHash -LiteralPath $exePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($exeBefore -ne $expectedExe) { throw 'Unexpected executable SHA256; no launch' }
$wrapperHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
$root = [IO.Path]::GetFullPath($OutputRoot)
[IO.Directory]::CreateDirectory($root) | Out-Null
$captureId = [guid]::NewGuid().ToString('N')
$dir = Join-Path $root ($Round + '-' + $captureId)
if (Test-Path -LiteralPath $dir) { throw 'Capture directory already exists' }
New-Item -ItemType Directory -Path $dir | Out-Null
$log = Join-Path $dir 'receiver.jsonl'
$summary = $log + '.summary.json'
$stdout = Join-Path $dir 'stdout.bin'
$stderr = Join-Path $dir 'stderr.bin'
$arguments = if ($SelfTest) { @('--selftest','--output',(Join-Path $dir 'selftest')) } else {
    @('--serve','--bind',$Bind,'--udp-port','49001','--tcp-port','49002','--seconds','300','--log',$log)
}
function QuoteArg([string]$value) {
    if ($value.Contains('"')) { throw 'Unsupported quote in argument' }
    return '"' + $value + '"'
}
function NowNs { return ([datetime]::UtcNow.Ticks - [long]621355968000000000) * [long]100 }
function WriteNew([string]$path, [byte[]]$bytes) {
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
    try { $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
}
$start = NowNs
$process = $null
$rc = $null
$spawnError = $null
try {
    $process = Start-Process -FilePath $exePath -ArgumentList (($arguments | ForEach-Object { QuoteArg $_ }) -join ' ') -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $null = $process.Handle
    Write-Output ("CAPTURE_STARTED round=" + $Round + " directory=" + $dir)
    $seen = 0
    while (-not $process.HasExited) {
        if (Test-Path -LiteralPath $stdout) {
            $lines = @(Get-Content -LiteralPath $stdout -Encoding UTF8)
            for ($i=$seen; $i -lt $lines.Count; $i++) { Write-Output $lines[$i] }
            $seen = $lines.Count
        }
        Start-Sleep -Milliseconds 200
        $process.Refresh()
    }
    $process.WaitForExit()
    $rc = $process.ExitCode
    # Drain the final lines even when exit happened between polling iterations.
    $lines = @(Get-Content -LiteralPath $stdout -Encoding UTF8)
    for ($i=$seen; $i -lt $lines.Count; $i++) { Write-Output $lines[$i] }

} catch { $spawnError = $_.Exception.Message }
$finish = NowNs
$exeAfter = (Get-FileHash -LiteralPath $exePath -Algorithm SHA256).Hash.ToLowerInvariant()
$hashes = @{}
foreach ($name in @('receiver.jsonl','receiver.jsonl.summary.json','stdout.bin','stderr.bin')) {
    $file = Join-Path $dir $name
    if (Test-Path -LiteralPath $file) {
        $hashes[$name] = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$receiverRun = $null
if (Test-Path -LiteralPath $summary) { $receiverRun = (Get-Content -LiteralPath $summary -Raw -Encoding UTF8 | ConvertFrom-Json).run_id }
$proof = [ordered]@{
    schema='witness-process-exit-v1'; mode=$(if($SelfTest){'SELFTEST'}else{'SERVE'})
    round=$Round; capture_id=$captureId; command_argv=@($exePath)+$arguments
    launched_pid=$(if($process){$process.Id}else{$null}); receiver_run_id=$receiverRun
    exit_code=$rc; spawn_error=$spawnError; started_utc_ns=$start; finished_utc_ns=$finish
    exe_before_sha256=$exeBefore; exe_after_sha256=$exeAfter; wrapper_sha256=$wrapperHash
    files=$hashes; production_gate='CLOSED'; certificate_written=$false
}
$utf8 = New-Object Text.UTF8Encoding($false)
WriteNew (Join-Path $dir 'process-exit.json') ($utf8.GetBytes(($proof | ConvertTo-Json -Depth 8) + [Environment]::NewLine))
foreach ($name in @('receiver.jsonl','receiver.jsonl.summary.json','stdout.bin','stderr.bin','process-exit.json')) {
    $file = Join-Path $dir $name
    if (Test-Path -LiteralPath $file) {
        WriteNew ($file+'.b64') ($utf8.GetBytes([Convert]::ToBase64String([IO.File]::ReadAllBytes($file))))
    }
}
Write-Output ("CAPTURE_FINISHED directory=" + $dir + " exit_code=" + $rc)
if ($null -eq $rc -or $spawnError) { exit 2 }
exit $rc
