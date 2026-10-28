$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$projectDir = Join-Path $PSScriptRoot 'DaiCaMinimal'
$compilerDir = Join-Path $PSScriptRoot 'compiler'
$archive = Join-Path $PSScriptRoot 'compiler.zip'
Invoke-WebRequest -Uri 'https://github.com/m0tral/EasyFace/releases/download/v4.23/EasyFace_Gen2_CompilerV423.zip' -OutFile $archive
$expected = '5b62773369c10c3402f369e8aa579f13393af359d0214c0d979464e5cc776cef'
if ((Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) { throw 'Compiler download checksum mismatch.' }
Expand-Archive -LiteralPath $archive -DestinationPath $compilerDir -Force
$outDir = Join-Path $projectDir 'output'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$target = Join-Path $outDir 'DaiCaMinimal.bin'
if (Test-Path $target) { Remove-Item $target }
$log = & (Join-Path $compilerDir 'Compiler.exe') -b (Join-Path $projectDir 'DaiCaMinimal.fprj') $outDir 'DaiCaMinimal.bin' '1461256429' 2>&1
$compilerExit = $LASTEXITCODE
$log | Out-Host
$log | Out-File (Join-Path $outDir 'build-log.txt') -Encoding utf8
if ($compilerExit -ne 0 -or !(Test-Path $target) -or (($log -join "`n") -match 'Error:')) { throw 'Compiler failed. See build-log.txt.' }
$bytes = [IO.File]::ReadAllBytes($target)
if ($bytes.Length -lt 100) { throw 'Output is too small.' }
# Match Mi Create ID assignment after compiler output.
$id = [Text.Encoding]::ASCII.GetBytes('928105001')
[Array]::Copy($id, 0, $bytes, 40, 9)
[IO.File]::WriteAllBytes($target, $bytes)
Get-FileHash $target -Algorithm SHA256 | Format-List | Out-String | Set-Content (Join-Path $outDir 'SHA256.txt')
Copy-Item (Join-Path $projectDir 'preview-full.png') $outDir
@'
Dai Ca Minimal — Redmi Watch 5 Lite ONLY (410 x 502)
24-hour time, Vietnamese weekday, DD/MM date.
Install DaiCaMinimal.bin through an already-paired Gadgetbridge on Android.
Compiled successfully on Windows; physical-watch behavior has not been tested.
'@ | Set-Content (Join-Path $outDir 'READ-ME.txt') -Encoding utf8
Write-Host "Created: $target ($($bytes.Length) bytes)"
