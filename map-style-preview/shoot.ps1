# Takes preview screenshots of each map style with Microsoft Edge (headless).
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
# Tiny local web server (no Python needed)
$py = Start-Job -ArgumentList $here -ScriptBlock { param($root)
  $types = @{ ".html"="text/html; charset=utf-8"; ".js"="application/javascript"; ".css"="text/css"; ".svg"="image/svg+xml"; ".png"="image/png" }
  $l = New-Object System.Net.HttpListener; $l.Prefixes.Add("http://127.0.0.1:8765/"); $l.Start()
  while ($true) { $c = $l.GetContext(); $p = Join-Path $root ([Uri]::UnescapeDataString($c.Request.Url.AbsolutePath.TrimStart("/")))
    if (Test-Path $p -PathType Leaf) { $b = [IO.File]::ReadAllBytes($p); $ext = [IO.Path]::GetExtension($p); if ($types[$ext]) { $c.Response.ContentType = $types[$ext] }; $c.Response.OutputStream.Write($b, 0, $b.Length) } else { $c.Response.StatusCode = 404 }
    $c.Response.Close() } }
Start-Sleep 2
New-Item -ItemType Directory -Force "$here\shots" | Out-Null
foreach ($s in "current","grey","light","night","faded") {
  foreach ($d in @(@("desk","1280,980","map-styles.html"), @("phone","600,860","phone.html"))) {
    $out = "$here\shots\$s-$($d[0]).png"
    & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 "--window-size=$($d[1])" "--screenshot=$out" --virtual-time-budget=12000 "http://127.0.0.1:8765/$($d[2])?style=$s&shot=1" | Out-Null
    Write-Output "saved $out"
  }
}
Stop-Job $py; Remove-Job $py -Force
