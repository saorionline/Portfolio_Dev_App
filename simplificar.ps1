# simplificar.ps1 - run once from the project folder:
#   powershell -ExecutionPolicy Bypass -File .\simplificar.ps1
# 1) creates branch "simplificacion"  2) deletes the old apps and files
# 3) checks Django, runs the tests and requests the page  4) opens the site
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
$log = Join-Path $PSScriptRoot "simplificar.log"
Set-Content -Path $log -Value "simplificar.ps1 - $(Get-Date -Format s)" -Encoding UTF8

function Log($msg) {
    Write-Host $msg
    Add-Content -Path $log -Value $msg -Encoding UTF8
}
function Run($cmd) {
    $out = cmd /c "$cmd 2>&1"
    $code = $LASTEXITCODE
    Log ("> $cmd  (exit $code)")
    if ($out) { Log (($out | Out-String).TrimEnd()) }
    return $code
}

Log "`n[1/4] Backup branch"
$current = (cmd /c "git branch --show-current").Trim()
Log "current branch: $current"
if ($current -ne "simplificacion") {
    cmd /c "git show-ref --verify --quiet refs/heads/simplificacion"
    if ($LASTEXITCODE -eq 0) { Run "git switch simplificacion" | Out-Null }
    else { Run "git switch -c simplificacion" | Out-Null }
}

Log "`n[2/4] Removing old apps and files"
$remove = @(
    "atlas_app", "core", "curriculum",
    "portfolio\admin.py", "portfolio\models.py", "portfolio\migrations",
    "curriculum.json", "initial_data.json", "portfolio_library.json",
    "db.sqlite3", "main.html", "main.js", "style.css"
)
foreach ($p in $remove) {
    if (Test-Path $p) {
        Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue
        if (Test-Path $p) { Log "  ! could not delete $p (is it open in another program?)" }
        else { Log "  - $p" }
    }
}
Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Log "  - all __pycache__ folders"

Log "`n[3/4] Verifying"
$okDjango = (Run "python -m django --version") -eq 0
$okCheck = $false; $okTest = $false; $okHttp = $false
if (-not $okDjango) {
    Log "Django is not installed for this Python. Run: python -m pip install -r requirements.txt"
} else {
    $okCheck = (Run "python manage.py check") -eq 0
    $okTest = (Run "python manage.py test portfolio -v 2") -eq 0

    $server = Start-Process python -ArgumentList "manage.py", "runserver", "--noreload", "8765" -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 6
    try {
        $page = Invoke-WebRequest "http://127.0.0.1:8765/" -UseBasicParsing
        $css = Invoke-WebRequest "http://127.0.0.1:8765/static/portfolio/style.css" -UseBasicParsing
        Log "GET /                          -> $($page.StatusCode) ($($page.Content.Length) chars)"
        Log "GET /static/portfolio/style.css -> $($css.StatusCode)"
        foreach ($t in "Nebula", "Phoenix", "Quantum", "Silverlining", "FastAPI", "Java &amp; Database Engineering") {
            Log ("  contains '$t': " + $page.Content.Contains($t))
        }
        $okHttp = ($page.StatusCode -eq 200) -and ($css.StatusCode -eq 200) -and $page.Content.Contains("Nebula")
    } catch {
        Log "HTTP error: $_"
    }
    if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force }
}

Log "`n[4/4] Summary"
Log "django: $okDjango | check: $okCheck | tests: $okTest | http: $okHttp"
Run "git status --short" | Out-Null

if ($okDjango -and $okCheck -and $okTest -and $okHttp) {
    Log "ALL OK - opening http://127.0.0.1:8000/"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot'; python manage.py runserver"
    Start-Sleep -Seconds 4
    Start-Process "http://127.0.0.1:8000/"
    Remove-Item $PSCommandPath -Force
} else {
    Log "SOMETHING FAILED - see simplificar.log"
}
