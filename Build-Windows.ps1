$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
Write-Host 'Downloading and verifying EasyFace compiler...'
Set-Location $PSScriptRoot
$projectDir = Join-Path $PSScriptRoot 'DaiCaMinimal'
$compilerDir = Join-Path $PSScriptRoot 'compiler'
$archive = Join-Path $PSScriptRoot 'compiler.zip'
Invoke-WebRequest -Uri 'https://github.com/m0tral/EasyFace/releases/download/v4.23/EasyFace_Gen2_CompilerV423.zip' -OutFile $archive -TimeoutSec 120
$expected = '5b62773369c10c3402f369e8aa579f13393af359d0214c0d979464e5cc776cef'
if ((Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) { throw 'Compiler download checksum mismatch.' }
Expand-Archive -LiteralPath $archive -DestinationPath $compilerDir -Force
$outDir = Join-Path $projectDir 'output'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$target = Join-Path $outDir 'DaiCaMinimal.bin'
if (Test-Path $target) { Remove-Item $target }
Write-Host 'Starting watchface compiler...'
$stdout = Join-Path $outDir 'compiler-stdout.txt'
$stderr = Join-Path $outDir 'compiler-stderr.txt'
$arguments = '-b "{0}" "{1}" "DaiCaMinimal.bin" "1461256429"' -f (Join-Path $projectDir 'DaiCaMinimal.fprj'), $outDir
$p = Start-Process -FilePath (Join-Path $compilerDir 'Compiler.exe') -WorkingDirectory $compilerDir -ArgumentList $arguments -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
if (!$p.WaitForExit(60000)) {
    Get-Process | Where-Object { $_.MainWindowTitle } | Select-Object Name, Id, MainWindowTitle | Out-File (Join-Path $outDir 'windows.txt')
    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
        $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bmp.Size)
        $bmp.Save((Join-Path $outDir 'compiler-screen.png'))
        $g.Dispose(); $bmp.Dispose()
    } catch { Write-Host $_ }
    Stop-Process -Id $p.Id -Force
    Get-Content $stdout, $stderr | Tee-Object -FilePath (Join-Path $outDir 'build-log.txt')
    throw 'Compiler timed out after 60 seconds. See diagnostics.'
}
$p.WaitForExit()
$log = Get-Content $stdout, $stderr
$log | Out-Host
$log | Out-File (Join-Path $outDir 'build-log.txt') -Encoding utf8
if (!(Test-Path $target) -or (($log -join "`n") -match 'Error:') -or (($log -join "`n") -notmatch 'No Errors')) { throw 'Compiler failed. See build-log.txt.' }
$bytes = [IO.File]::ReadAllBytes($target)
if ($bytes.Length -lt 100) { throw 'Output is too small.' }
# Match Mi Create ID assignment after compiler output.
$id = [Text.Encoding]::ASCII.GetBytes('928105003')
[Array]::Copy($id, 0, $bytes, 40, 9)
[IO.File]::WriteAllBytes($target, $bytes)
Get-FileHash $target -Algorithm SHA256 | Format-List | Out-String | Set-Content (Join-Path $outDir 'SHA256.txt')
Copy-Item (Join-Path $projectDir 'preview-full.png') $outDir
Copy-Item (Join-Path $projectDir 'AOD/preview-full.png') (Join-Path $outDir 'preview-aod.png')
@'
Dai Ca Minimal — Redmi Watch 5 Lite ONLY (410 x 502)
Stacked 12-hour time, no AM/PM or icons. Vietnamese weekday, DD/MM and battery percentage. Outline-only AOD.
Install DaiCaMinimal.bin through an already-paired Gadgetbridge on Android.
Compiled successfully on Windows; physical-watch behavior has not been tested.
'@ | Set-Content (Join-Path $outDir 'READ-ME.txt') -Encoding utf8
Write-Host "Created: $target ($($bytes.Length) bytes)"
