# Backup Guide — UNKNOWN Beginner CTF

This describes exactly what to back up in **this** repository/deployment, using
the actual Docker Compose service names defined in `docker-compose.yml`:

- `ctfd` — the application
- `db` — MariaDB 10.11 (database name `ctfd`)
- `cache` — Redis 4
- `nginx` — reverse proxy
- `permissions` — one-shot init container (nothing to back up)

## 1. What is already tracked by Git

These live in the repository and do **not** need a separate backup beyond
your normal Git remote/history:

- Application code (`CTFd/`)
- Theme templates and CSS (`CTFd/themes/core`, `CTFd/themes/admin`)
- `docker-compose.yml`, `Dockerfile`, `conf/`
- This `operation/` documentation

## 2. What is NOT tracked by Git (must be backed up separately)

Per `.gitignore`, the following are bind-mounted to `.data/` on the host and
are **not** committed:

| Path                  | Contents                                                                     |
| --------------------- | ---------------------------------------------------------------------------- |
| `.data/mysql/`        | MariaDB data directory (users, challenges, scores, submissions — everything) |
| `.data/CTFd/uploads/` | Uploaded challenge files, imported CSVs, any player-uploaded assets          |
| `.data/CTFd/logs/`    | Application logs (nice to keep for incident review, not critical)            |
| `.data/redis/`        | Redis cache/session data (safe to lose — it's a cache, not source of truth)  |

**The two that matter are `.data/mysql/` and `.data/CTFd/uploads/`.** Everything
a participant did — accounts, solves, scores — lives in `.data/mysql/`.
Challenge files participants download live in `.data/CTFd/uploads/`.

Also check for **any Dockerized challenge servers** you run separately from
this stack (web/pwn challenge containers). Their state (if any) and their
compose/config files are not covered by this guide — document and back them
up separately if they hold state.

## 3. Secrets — never put these in Git

Do not commit, or write into any file that gets committed:

- The real admin account password
- `MARIADB_ROOT_PASSWORD` / `MARIADB_PASSWORD` values (currently set directly
  in `docker-compose.yml` for this deployment — treat that file as sensitive
  if its values are ever changed from the placeholder dev values)
- Any `SECRET_KEY` / API keys
- A full raw `.env` file, if one is introduced later — commit `.env.example`
  with placeholder values instead

## 4. Backup commands (run from the `platform/` project root)

### Database dump (hot, while running)

```bash
docker compose exec db sh -c 'exec mysqldump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' > backup_$(date +%Y%m%d_%H%M).sql
```

This reads the credentials from the `db` container's own environment, so the
command never has the password typed into your shell history.

### Uploads (challenge files)

```bash
tar -czf uploads_$(date +%Y%m%d_%H%M).tar.gz -C .data/CTFd uploads
```

### Full data directory (belt-and-suspenders, container stopped)

Only do this with the stack stopped, so MariaDB isn't mid-write:

```bash
docker compose stop
tar -czf full-data_$(date +%Y%m%d_%H%M).tar.gz .data
docker compose start
```

Prefer the live `mysqldump` above when the event is running and you can't
take the stack down; use the full stop-and-tar version for routine backups
outside event hours.

Store backups **outside** the `platform/` working directory (a separate
drive, bucket, or backup host) — a backup sitting next to a corrupted
`.data/` volume doesn't help if the disk itself fails.

## 5. When to back up

### Before the event (setup phase)

- Once challenges, categories, points and hints are finalized.
- Once test accounts are created and verified.
- Label this backup clearly, e.g. `backup_pre-event_YYYYMMDD.sql` — this is
  your rollback point if something goes wrong during final setup.

### Right before the event goes live

- Immediately before flipping registration/challenges to public.
- This is the backup you restore to if you need to "reset the clock" and
  start the event over from a clean state.

### During the event

- Periodically (e.g. every 30–60 minutes for a multi-hour event) via the
  `mysqldump` command above. Cheap, fast, and lets you recover from an
  operator mistake without losing hours of participant progress.

### After the event

- One final `mysqldump` + uploads tarball immediately after the scoreboard
  is frozen/finalized — this is your permanent record of final scores and
  is what you restore from if you need to regenerate certificates, resolve
  a scoring dispute, or produce a report afterward.
- Keep this one indefinitely (or per your event's data retention policy).
