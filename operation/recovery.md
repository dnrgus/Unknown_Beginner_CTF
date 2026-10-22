# Recovery Guide — UNKNOWN Beginner CTF

Use this to bring the platform back up from scratch (new machine) or after a
serious failure, using the actual service names in `docker-compose.yml`
(`ctfd`, `db`, `cache`, `nginx`, `permissions`).

Read [backup.md](backup.md) first if you haven't — this guide assumes you
have a database dump (`.sql`) and/or an uploads tarball produced by it.

## 1. Get the code

```bash
git clone <this repository's URL> platform
cd platform
```

If you're restoring on the _same_ machine after a failure, you likely
already have the working directory — skip to step 3, but confirm
`git status` is clean before doing anything destructive.

## 2. Restore configuration

This deployment does not use a `.env` file — the database credentials and
app settings are set directly as `environment:` values in
`docker-compose.yml`. Confirm that file matches what you expect (service
names, ports, `MARIADB_*` values) before starting anything. If a `.env.example`
is introduced later, copy it to `.env` and fill in real values there instead —
never commit the filled-in `.env`.

Do **not** recreate `.data/` by hand — it will be created automatically as
empty bind-mount directories the first time Docker starts, and an empty
`.data/mysql` means "start MariaDB from nothing," which is only correct if
you intend to restore a dump into it afterward (step 5).

## 3. Start Docker

```bash
docker compose up -d
```

This starts `permissions` (one-shot, fixes ownership on `.data/CTFd/logs`
and `.data/CTFd/uploads`), then `db`, `cache`, `ctfd`, and `nginx`.

Check everything is healthy:

```bash
docker compose ps
docker compose logs -f ctfd
```

On a **first-ever** start, MariaDB will initialize a fresh empty database
using the `MARIADB_*` values in `docker-compose.yml`, and CTFd will run its
own migrations against it. If you are restoring from a backup, keep reading
before touching the running app.

## 4. Restore the database

Wait for the `db` container to be up (`docker compose ps` shows it running,
or `docker compose logs db` shows it accepted connections), then:

```bash
cat backup_YYYYMMDD_HHMM.sql | docker compose exec -T db sh -c 'exec mysql -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"'
```

This replays the dump into the running `ctfd` database using the
container's own credentials. If the database already has tables from a
fresh `docker compose up`, this will insert on top of / conflict with them —
for a clean restore, stop the stack, delete `.data/mysql/` (only if you are
certain you don't need what's in it), and start again so MariaDB initializes
empty before you restore.

## 5. Restore uploads (challenge files)

```bash
tar -xzf uploads_YYYYMMDD_HHMM.tar.gz -C .data/CTFd
```

This should recreate `.data/CTFd/uploads/...` with the original files. After
extracting, re-run the `permissions` fix-up so the `ctfd` container can read
them:

```bash
docker compose up permissions
docker compose restart ctfd
```

## 6. Confirm it's actually working

Don't declare recovery done until you've checked, logged in as a real
(non-admin) test account where possible:

- [ ] `/` (Home) loads
- [ ] `/challenges` shows the expected challenges
- [ ] A known-good flag submits as **correct** on a test challenge
- [ ] `/scoreboard` shows the expected standings (matches what you backed up)
- [ ] `/admin` login works for the real admin account
- [ ] Admin → Users shows the expected user count
- [ ] Any separately-hosted challenge servers (web/pwn instances) are back
      up and reachable — these are outside this compose stack and are not
      restored by the steps above

If any of these fail, check `docker compose logs ctfd` and `docker compose
logs db` before making further changes.

## 7. What this guide does not cover

- Restoring separately-hosted dynamic/Docker-based challenge instances —
  document and recover those per their own setup.
- Rotating secrets after a suspected compromise — that's a security incident,
  not a routine recovery; change the admin password and any exposed
  credentials directly, and log it in `incident-log.md`.
