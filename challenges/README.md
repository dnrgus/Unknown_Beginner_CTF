# UNKNOWN Beginner CTF Challenges

This directory contains 18 beginner-friendly challenges built from the UNKNOWN Beginner CTF plan.

## Run Services

Web:

```bash
docker compose -f challenges/web/docker-compose.yml up -d --build
```

Pwn:

```bash
docker compose -f challenges/pwn/docker-compose.yml up -d --build
```

Seed all challenges into CTFd:

```bash
docker compose exec -T -w /opt/CTFd -e PYTHONPATH=/opt/CTFd ctfd python scripts/seed_unknown_all_challenges.py
```

## Challenge Table

| Category | Challenge | Difficulty | Concept | Expected Solve Time |
| --- | --- | --- | --- | --- |
| Web | 동아리 홈페이지 | Easy | HTML source / DevTools | 5-10 min |
| Web | 나는 관리자다 | Easy | Cookie tampering | 5-10 min |
| Web | 로그인 좀 해줘 | Easy+ | Basic SQL injection | 15-25 min |
| Pwn | 비밀번호를 까먹었다 | Easy | strings / binary observation | 5-10 min |
| Pwn | 넘치면 안 돼! | Easy | Stack buffer overflow | 10-20 min |
| Pwn | 절대 실행되지 않는 함수 | Easy+ | ret2win | 20-30 min |
| Reversing | 비밀번호 어디 갔지? | Easy | strings | 5-10 min |
| Reversing | 정답 검사기 | Easy | Decompiler / char checks | 10-20 min |
| Reversing | 암호화했으니 안전해 | Easy+ | XOR array recovery | 15-25 min |
| Crypto | 카이사르의 비밀편지 | Easy | Caesar cipher | 5-10 min |
| Crypto | 몇 번을 숨긴 거야? | Easy | Encoding layers | 10-15 min |
| Crypto | XOR이면 암호지! | Easy+ | 1-byte XOR brute force | 15-25 min |
| OSINT | 닉네임은 하나면 충분해 | Easy | Username pivot | 5-10 min |
| OSINT | 여기가 어디게? | Easy | Geolocation clues | 10-15 min |
| OSINT | 지웠으니까 괜찮겠지? | Easy+ | Git history | 15-25 min |
| Misc | 분명 파일이 있었는데 | Easy | Hidden file in archive | 5-10 min |
| Misc | 나는 TXT입니다 | Easy | File signature | 5-10 min |
| Misc | 사진에는 사진만 있다 | Easy+ | Image metadata | 10-20 min |

## Verification

Every challenge has:

- `README.md`
- `challenge/` files when participant files are needed
- `deploy/` files for service challenges
- `solution/solve.py`
- `solution/writeup.md`
- two staged hints in the CTFd seed script

Target state: `18/18 Challenges Verified`.
