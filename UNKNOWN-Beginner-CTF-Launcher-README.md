# UNKNOWN Beginner CTF Windows 런처

## 파일 구성

- `Launch-UNKNOWN-Beginner-CTF.ps1`: 런처 본체 로직
- `Start-UNKNOWN-Beginner-CTF.bat`: 더블클릭용 실행 파일

## 사용 방법

`Start-UNKNOWN-Beginner-CTF.bat`을 더블클릭하세요.

런처는 다음 순서로 동작합니다.

1. `C:\Users\dnrgu\OneDrive\Desktop\intro-ctf\platform` 폴더로 이동
2. Docker Compose로 CTFd 스택(nginx / CTFd / DB / Redis)을 실행
3. `challenges/web/docker-compose.yml`의 Web 챌린지 컨테이너(WEB-01~03)를 실행
4. `http://localhost:80`(CTFd)과 각 Web 챌린지 포트(8101~8103)가 응답할 때까지 대기
5. Cloudflare Quick Tunnel을 **CTFd 1개 + Web 챌린지 3개, 총 4개** 생성
6. 각 터널의 `https://*.trycloudflare.com` 주소를 추출
7. CTFd 접속 주소를 기본 브라우저로 자동 오픈
8. 런처 창에서 Enter를 누르기 전까지 모든 터널을 유지

## 외부 접속 주소

런처가 준비되면 아래와 같이 4개의 주소가 출력됩니다. 참가자에게는 CTFd 주소와 함께, 문제별 접속 주소도 같이 안내해야 합니다(CTFd 문제 설명에 있는 `localhost:810x` 주소는 참가자 PC 기준이 아니라 서버 PC 기준이라 그대로는 접속이 안 됩니다).

```
[CTFd]                   https://aaaa-bbbb-cccc.trycloudflare.com
[WEB-01 Source Hunter]   https://dddd-eeee-ffff.trycloudflare.com
[WEB-02 Cookie Monster]  https://gggg-hhhh-iiii.trycloudflare.com
[WEB-03 Baby SQL]        https://jjjj-kkkk-llll.trycloudflare.com
```

> Pwn 문제(8201~8203)는 HTTP가 아니라 TCP(`nc`) 기반이라 Cloudflare Quick Tunnel로 그대로 뚫을 수 없습니다. 현재 런처는 Pwn 문제를 외부에 노출하지 않습니다. 필요하면 별도 방식(named tunnel + TCP, 또는 VPN 등)으로 추가 작업이 필요합니다.

## 요구 사항

- Docker Desktop
- cloudflared

관리자 권한 PowerShell에서 cloudflared 설치:

```powershell
winget install --id Cloudflare.cloudflared
```

## 자가 진단 (Self Test)

Docker나 cloudflared를 실제로 실행하지 않고, 필요한 파일/명령어가 있는지만 확인합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Launch-UNKNOWN-Beginner-CTF.ps1 -SelfTest
```

## 컨테이너 종료

런처 창에서 Enter를 누르면 Cloudflare 터널만 종료되고, Docker 컨테이너는 계속 켜져 있습니다. 완전히 끄려면 플랫폼 폴더에서 다음을 실행하세요.

```powershell
docker compose down
docker compose -f challenges\web\docker-compose.yml down
```

## 단일 EXE 패키징 (선택 사항)

가장 간단하고 안정적인 방법은 바탕화면 런처로 BAT 파일을 그대로 쓰는 것입니다. 그래도 `.exe` 하나로 묶고 싶다면 PS2EXE를 사용하세요.

```powershell
Install-Module ps2exe -Scope CurrentUser
Invoke-ps2exe .\Launch-UNKNOWN-Beginner-CTF.ps1 .\UNKNOWN-Beginner-CTF-Launcher.exe -noConsole:$false -title "UNKNOWN Beginner CTF Launcher"
```

이 EXE는 PowerShell 스크립트를 감싼 것뿐이므로, 실행할 PC에는 여전히 Docker Desktop과 cloudflared가 설치돼 있어야 합니다.
