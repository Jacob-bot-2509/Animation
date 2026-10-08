$ErrorActionPreference='Stop'
$project=[IO.Path]::GetFullPath('D:\Animation-Model-Training')
$out=Join-Path $project 'reviews\codex-supervision\2026-10-06-scene-repair-takeover'
$chunkRoot=[IO.Path]::GetFullPath((Join-Path $project 'reviews\2026-10-06-scene-standard-sweep\chunks'))
$originalRoot=[IO.Path]::GetFullPath((Join-Path $out 'original-inputs'))
$plan=Get-Content -LiteralPath (Join-Path $out 'restore-plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$locked=[Collections.Generic.List[object]]::new()
$sha=[Security.Cryptography.SHA256]::Create()
$didWrite=$false
function Digest([byte[]]$bytes){return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()}
function ReadLocked($stream){$stream.Position=0; $m=[IO.MemoryStream]::new(); try{$stream.CopyTo($m);return ,$m.ToArray()}finally{$m.Dispose()}}
try {
 foreach($entry in $plan.files){
  $target=[IO.Path]::GetFullPath((Join-Path $project $entry.path))
  $origin=[IO.Path]::GetFullPath((Join-Path $project $entry.original_path))
  if([IO.Path]::GetDirectoryName($target) -ne $chunkRoot -or [IO.Path]::GetFileName($target) -notmatch '^(chunk-\d{2}|listing)\.json$'){throw 'Unexpected restore target'}
  if([IO.Path]::GetDirectoryName($origin) -ne $originalRoot){throw 'Unexpected archive path'}
  $original=[IO.File]::ReadAllBytes($origin)
  if((Digest $original) -ne $entry.original_raw_sha256){throw 'Original archive SHA mismatch'}
  $attrs=[IO.File]::GetAttributes($target)
  $stream=[IO.File]::Open($target,[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
  $item=[PSCustomObject]@{path=$target; entry=$entry; stream=$stream; original=$original; attributes=$attrs; before=$null}
  $locked.Add($item)
  $item.before=ReadLocked $stream
  if((Digest $item.before) -ne $entry.current_raw_sha256){throw 'Writer changed input after capture; no restore performed'}
 }
 foreach($item in $locked){
  $didWrite=$true
  $item.stream.Position=0; $item.stream.SetLength(0)
  $item.stream.Write($item.original,0,$item.original.Length);$item.stream.Flush($true)
  if((Digest (ReadLocked $item.stream)) -ne $item.entry.original_raw_sha256){throw 'Restored bytes mismatch'}
  [IO.File]::SetAttributes($item.path,($item.attributes -bor [IO.FileAttributes]::ReadOnly))
 }
}catch{
 if($didWrite){
  foreach($item in $locked){
   [IO.File]::SetAttributes($item.path,$item.attributes)
   $item.stream.Position=0;$item.stream.SetLength(0);$item.stream.Write($item.before,0,$item.before.Length);$item.stream.Flush($true)
  }
 }
 throw
}finally{
 foreach($item in $locked){$item.stream.Dispose()}
}
$results=@()
foreach($item in $locked){
 $bytes=[IO.File]::ReadAllBytes($item.path)
 if((Digest $bytes) -ne $item.entry.original_raw_sha256){throw 'Post-close restored SHA mismatch'}
 $denied=$false
 try{$probe=[IO.File]::Open($item.path,[IO.FileMode]::Open,[IO.FileAccess]::Write,[IO.FileShare]::Read);$probe.Dispose()}
 catch [UnauthorizedAccessException] {$denied=$true}
 if(-not $denied){throw 'Historical input write protection not effective'}
 $results+=[PSCustomObject]@{path=$item.entry.path; raw_sha256=(Digest $bytes); restored=$true; read_only=$true; ordinary_write_open_denied=$denied}
}
$record=[PSCustomObject]@{schema='historical-input-restoration-v1'; checked_at=[DateTimeOffset]::Now.ToString('o'); status='RESTORED_AND_READONLY'; files=$results; stopped_claude_process=$false; claude_stop_ack_received=$false; file_acl_modified=$false; read_only_guard_reversible=$true; changed_scenes_preserved=18}
$p=Join-Path $out 'input-restoration-verification.json'
if(Test-Path -LiteralPath $p){throw 'Restoration result exists'}
[IO.File]::WriteAllText($p,($record|ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$sha.Dispose()
[PSCustomObject]@{restored_files=$results.Count; sha_match=$true; write_open_denied=$true; acl_changed=$false; candidates_preserved=18} | ConvertTo-Json
