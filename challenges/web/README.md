# UNKNOWN Beginner CTF - Web Phase

Phase 1 creates three beginner Web challenges from the production plan.

| Challenge             | Difficulty | Concept                | Local URL             | Expected Time |
| --------------------- | ---------- | ---------------------- | --------------------- | ------------- |
| WEB-01 Source Hunter  | Easy       | HTML source / DevTools | http://localhost:8101 | 5-10 min      |
| WEB-02 Cookie Monster | Easy       | Cookie tampering       | http://localhost:8102 | 10-15 min     |
| WEB-03 Baby SQL       | Easy+      | Basic SQL Injection    | http://localhost:8103 | 15-25 min     |

Run the services:

```bash
docker compose -f challenges/web/docker-compose.yml up -d --build
```

Verify intended solves:

```bash
python challenges/web/source-hunter/solution/solve.py http://localhost:8101
python challenges/web/cookie-monster/solution/solve.py http://localhost:8102
python challenges/web/baby-sql/solution/solve.py http://localhost:8103
```

Seed CTFd challenge entries:

```bash
docker compose exec ctfd python /opt/CTFd/scripts/seed_unknown_web_challenges.py
```
