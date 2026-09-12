param(
    [string]$PlatformPath = "C:\Users\dnrgu\OneDrive\Desktop\intro-ctf\platform",
    [string]$LocalUrl = "http://localhost:80",
    [int]$ReadyTimeoutSec = 240,
    [switch]$SelfTest
)

$ErrorActionPreference = "Stop"
$cloudflaredProcesses = @()
$DockerExe = $null
$CloudflaredExe = $null

$WebChallenges = @(
    @{ Name = "WEB-01 Source Hunter"; LocalUrl = "http://localhost:8101" },
    @{ Name = "WEB-02 Cookie Monster"; LocalUrl = "http://localhost:8102" },
    @{ Name = "WEB-03 Baby SQL"; LocalUrl = "http://localhost:8103" }
)

try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
}
catch {
    # Older consoles can ignore encoding changes; the launcher can still run.
}

function Write-Section {
    param([string]$Text)
    Write-Host ""
    Write-Host ("=" * 78) -ForegroundColor Cyan
    Write-Host ("  " + $Text) -ForegroundColor Cyan
    Write-Host ("=" * 78) -ForegroundColor Cyan
}

function Write-Info {
    param([string]$Text)
    Write-Host ("[INFO] " + $Text) -ForegroundColor Gray
}

function Write-Ok {
    param([string]$Text)
    Write-Host ("[OK]   " + $Text) -ForegroundColor Green
}

function Write-Warn {
    param([string]$Text)
    Write-Host ("[WARN] " + $Text) -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Text)
    Write-Host ("[FAIL] " + $Text) -ForegroundColor Red
}

function Wait-EnterThenExit {
    param([int]$Code = 1)
    Write-Host ""
    Read-Host "창을 닫으려면 Enter를 누르세요"
    exit $Code
}

function Resolve-ToolPath {
    param(
        [string]$Name,
        [string[]]$Candidates,
        [string]$InstallHint
    )

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $command) {
        foreach ($candidate in $Candidates) {
            if ($candidate -and (Test-Path -LiteralPath $candidate)) {
                return $candidate
            }
        }
        throw "$Name 을(를) 찾을 수 없습니다. $InstallHint"
    }
    return $command.Source
}

function Invoke-CheckedCommand {
    param(
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory = $PlatformPath
    )

    $output = & $FilePath @ArgumentList 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        $text = ($output | Out-String).Trim()
        if ([string]::IsNullOrWhiteSpace($text)) {
            $text = "출력 없음"
        }
        throw "명령 실행 실패: $FilePath $($ArgumentList -join ' ')`n$text"
    }
    return $output
}

function Test-DockerReady {
    try {
        & $script:DockerExe info *> $null
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        return $false
    }
}

function Start-DockerDesktopIfNeeded {
    if (Test-DockerReady) {
        Write-Ok "Docker가 실행 중입니다."
        return
    }

    Write-Warn "Docker가 아직 실행되지 않았습니다. Docker Desktop을 찾아서 시작해볼게요."
    $dockerDesktopCandidates = @(
        "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe",
        "${env:ProgramFiles(x86)}\Docker\Docker\Docker Desktop.exe",
        "$env:LOCALAPPDATA\Docker\Docker Desktop.exe",
        "$env:LOCALAPPDATA\Programs\DockerDesktop\Docker Desktop.exe"
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

    if ($dockerDesktopCandidates.Count -gt 0) {
        Start-Process -FilePath $dockerDesktopCandidates[0] | Out-Null
        Write-Info "Docker Desktop 시작 요청을 보냈습니다. 준비될 때까지 기다립니다."
    }
    else {
        throw "Docker Desktop이 실행 중이 아니고 설치 위치도 찾지 못했습니다. Docker Desktop을 먼저 실행한 뒤 다시 시도하세요."
    }

    $deadline = (Get-Date).AddSeconds(150)
    while ((Get-Date) -lt $deadline) {
        if (Test-DockerReady) {
            Write-Ok "Docker가 준비됐습니다."
            return
        }
        Start-Sleep -Seconds 3
        Write-Host "." -NoNewline -ForegroundColor DarkGray
    }
    Write-Host ""
    throw "Docker Desktop이 제한 시간 안에 준비되지 않았습니다. Docker Desktop 창에서 오류가 있는지 확인하세요."
}

function Test-Port80 {
    try {
        $listeners = Get-NetTCPConnection -LocalPort 80 -State Listen -ErrorAction SilentlyContinue
        if ($listeners) {
            $owners = $listeners |
                Select-Object -ExpandProperty OwningProcess -Unique |
                ForEach-Object {
                    $process = Get-Process -Id $_ -ErrorAction SilentlyContinue
                    if ($process) { "$($process.ProcessName) (PID $($_))" } else { "PID $($_)" }
                }
            Write-Warn "포트 80이 이미 사용 중입니다: $($owners -join ', ')"
            Write-Warn "이미 이 CTF가 켜져 있는 상태라면 괜찮지만, 다른 프로그램이면 Docker Compose가 실패할 수 있습니다."
        }
        else {
            Write-Ok "포트 80은 비어 있습니다."
        }
    }
    catch {
        Write-Warn "포트 80 상태를 확인하지 못했습니다. 계속 진행합니다."
    }
}

function Wait-CtfReady {
    param([string]$Url, [int]$TimeoutSec, [string]$Label = "CTF 웹서버")

    Write-Info "$Label 가 응답할 때까지 기다립니다: $Url"
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $lastError = $null

    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -MaximumRedirection 0 -ErrorAction Stop
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                Write-Ok "$Label 가 응답합니다. HTTP $($response.StatusCode)"
                return
            }
        }
        catch {
            $lastError = $_.Exception.Message
            if ($_.Exception.Response -and $_.Exception.Response.StatusCode.value__ -lt 500) {
                Write-Ok "$Label 가 응답합니다. HTTP $($_.Exception.Response.StatusCode.value__)"
                return
            }
        }

        Write-Host "." -NoNewline -ForegroundColor DarkGray
        Start-Sleep -Seconds 3
    }

    Write-Host ""
    $composeStatus = (& $script:DockerExe compose ps 2>&1 | Out-String).Trim()
    throw "$Label 가 제한 시간 안에 준비되지 않았습니다.`n마지막 상태: $lastError`n`nDocker Compose 상태:`n$composeStatus"
}

function Start-CloudflaredTunnel {
    param([string]$Url, [string]$Label = "Cloudflare Quick Tunnel")

    $tempLog = Join-Path $env:TEMP ("unknown-ctf-cloudflared-" + [guid]::NewGuid().ToString("N") + ".log")
    $arguments = @("tunnel", "--url", $Url, "--no-autoupdate", "--logfile", $tempLog)

    Write-Info "$Label 을(를) 시작합니다. ($Url)"
    $process = Start-Process -FilePath $script:CloudflaredExe -ArgumentList $arguments -PassThru -WindowStyle Hidden
    $script:cloudflaredProcesses += $process

    $deadline = (Get-Date).AddSeconds(90)
    $urlPattern = "https://[a-zA-Z0-9-]+\.trycloudflare\.com"

    while ((Get-Date) -lt $deadline) {
        if ($process.HasExited) {
            $logText = if (Test-Path -LiteralPath $tempLog) { Get-Content -LiteralPath $tempLog -Raw } else { "" }
            throw "$Label 이(가) 바로 종료되었습니다.`n$logText"
        }

        if (Test-Path -LiteralPath $tempLog) {
            $logText = Get-Content -LiteralPath $tempLog -Raw
            $match = [regex]::Match($logText, $urlPattern)
            if ($match.Success) {
                return $match.Value
            }
        }

        Start-Sleep -Seconds 1
    }

    $logTail = if (Test-Path -LiteralPath $tempLog) {
        (Get-Content -LiteralPath $tempLog -Tail 80 | Out-String).Trim()
    }
    else {
        "cloudflared 로그 파일이 생성되지 않았습니다."
    }
    throw "$Label 의 trycloudflare.com 주소를 제한 시간 안에 찾지 못했습니다.`n$logTail"
}

function Stop-Cloudflared {
    foreach ($process in $script:cloudflaredProcesses) {
        if ($process -and -not $process.HasExited) {
            Write-Info "cloudflared 터널을 종료합니다. (PID $($process.Id))"
            try {
                $process.CloseMainWindow() | Out-Null
                Start-Sleep -Milliseconds 500
                if (-not $process.HasExited) {
                    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
                }
            }
            catch {
                Write-Warn "cloudflared 종료 중 문제가 있었지만 계속 마무리합니다: $($_.Exception.Message)"
            }
        }
    }
}

try {
    Write-Section "UNKNOWN Beginner CTF Launcher"

    if ($SelfTest) {
        Write-Info "자가 진단 모드입니다. 서버와 터널은 시작하지 않습니다."
    }

    if (-not (Test-Path -LiteralPath $PlatformPath)) {
        throw "CTF 폴더를 찾을 수 없습니다: $PlatformPath"
    }

    $composeFile = Join-Path $PlatformPath "docker-compose.yml"
    if (-not (Test-Path -LiteralPath $composeFile)) {
        throw "docker-compose.yml을 찾을 수 없습니다: $composeFile"
    }

    $script:DockerExe = Resolve-ToolPath `
        -Name "docker" `
        -Candidates @(
            "$env:ProgramFiles\Docker\Docker\resources\bin\docker.exe",
            "${env:ProgramFiles(x86)}\Docker\Docker\resources\bin\docker.exe"
        ) `
        -InstallHint "Docker Desktop을 설치하고 다시 실행하세요."

    $script:CloudflaredExe = Resolve-ToolPath `
        -Name "cloudflared" `
        -Candidates @(
            "$env:ProgramFiles\cloudflared\cloudflared.exe",
            "$env:LOCALAPPDATA\Microsoft\WinGet\Links\cloudflared.exe",
            "$env:LOCALAPPDATA\Programs\cloudflared\cloudflared.exe"
        ) `
        -InstallHint "관리자 PowerShell에서 winget install --id Cloudflare.cloudflared 를 실행하세요."

    Write-Ok "Docker 명령을 찾았습니다: $script:DockerExe"
    Write-Ok "cloudflared 명령을 찾았습니다: $script:CloudflaredExe"

    if ($SelfTest) {
        Write-Ok "자가 진단을 통과했습니다."
        Wait-EnterThenExit 0
    }

    Set-Location -LiteralPath $PlatformPath

    Start-DockerDesktopIfNeeded
    Test-Port80

    Write-Section "Docker Compose 시작"
    Write-Info "이미 실행 중인 컨테이너는 재사용하고, 필요한 이미지는 빌드합니다."
    Invoke-CheckedCommand -FilePath $script:DockerExe -ArgumentList @("compose", "up", "-d", "--build") | Out-Null
    Write-Ok "Docker Compose 시작 요청이 완료됐습니다."

    $webComposeFile = Join-Path $PlatformPath "challenges\web\docker-compose.yml"
    if (Test-Path -LiteralPath $webComposeFile) {
        Write-Info "Web 챌린지 컨테이너를 시작합니다."
        Invoke-CheckedCommand -FilePath $script:DockerExe -ArgumentList @("compose", "-f", $webComposeFile, "up", "-d", "--build") | Out-Null
        Write-Ok "Web 챌린지 컨테이너 시작 요청이 완료됐습니다."
    }
    else {
        Write-Warn "Web 챌린지 docker-compose.yml을 찾지 못해 건너뜁니다: $webComposeFile"
    }

    Wait-CtfReady -Url $LocalUrl -TimeoutSec $ReadyTimeoutSec -Label "CTFd 웹서버"

    foreach ($challenge in $WebChallenges) {
        Wait-CtfReady -Url $challenge.LocalUrl -TimeoutSec $ReadyTimeoutSec -Label $challenge.Name
    }

    Write-Section "외부 접속 주소 만들기"
    $publicUrl = Start-CloudflaredTunnel -Url $LocalUrl -Label "CTFd 터널"

    $publicChallengeUrls = @()
    foreach ($challenge in $WebChallenges) {
        $url = Start-CloudflaredTunnel -Url $challenge.LocalUrl -Label "$($challenge.Name) 터널"
        $publicChallengeUrls += @{ Name = $challenge.Name; Url = $url }
    }

    Write-Host ""
    Write-Host ("#" * 78) -ForegroundColor Green
    Write-Host "  UNKNOWN Beginner CTF 접속 주소" -ForegroundColor Green
    Write-Host ""
    Write-Host "  [CTFd]  $publicUrl" -ForegroundColor White -BackgroundColor DarkGreen
    foreach ($entry in $publicChallengeUrls) {
        Write-Host "  [$($entry.Name)]  $($entry.Url)" -ForegroundColor White -BackgroundColor DarkGreen
    }
    Write-Host ""
    Write-Host ("#" * 78) -ForegroundColor Green
    Write-Host ""

    Write-Info "기본 브라우저로 CTFd 접속 주소를 엽니다."
    Start-Process $publicUrl

    Write-Warn "이 창을 닫거나 Enter를 누르면 외부 접속 터널이 종료됩니다."
    Write-Warn "Docker 컨테이너는 계속 켜둘 수 있습니다. 완전히 끄려면 CTF 폴더에서 docker compose down을 실행하세요."
    Read-Host "터널을 종료하려면 Enter를 누르세요"
}
catch {
    Write-Host ""
    Write-Fail $_.Exception.Message
    Write-Host ""
    Write-Host "빠른 해결 팁:" -ForegroundColor Yellow
    Write-Host "- Docker Desktop을 먼저 켠 뒤 다시 실행해보세요."
    Write-Host "- cloudflared가 없다면 관리자 PowerShell에서 winget install --id Cloudflare.cloudflared 를 실행하세요."
    Write-Host "- 포트 80을 다른 프로그램이 쓰고 있다면 그 프로그램을 종료하세요."
    Write-Host "- Docker Compose 실패가 반복되면 Docker Desktop에서 Containers/Images 상태를 확인하세요."
    Wait-EnterThenExit 1
}
finally {
    Stop-Cloudflared
}
