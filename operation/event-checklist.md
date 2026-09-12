# Event Checklist — UNKNOWN Beginner CTF

A run-through checklist for the operator. See also [backup.md](backup.md)
and [recovery.md](recovery.md). Log anything that goes wrong in
[incident-log.md](incident-log.md).

## Quick Event Check (do this any time you want a fast sanity pass)

- [ ] Registration status is what you intend (Admin → Statistics shows
      `REGISTRATION` OPEN/CLOSED, or check Admin → Config)
- [ ] Challenge Visibility is what you intend (`CHALLENGES` PUBLIC/PRIVATE
      on the Admin → Statistics dashboard)
- [ ] Scoreboard Visibility is what you intend (`SCOREBOARD` on the same
      dashboard)
- [ ] Test account(s) still work and are excluded from the real scoreboard
      (hidden/banned as appropriate) — do not leave a scored test account
      showing at #1
- [ ] Player-facing files download correctly for at least one file-based
      challenge
- [ ] Any separately-hosted dynamic/web challenge servers respond
- [ ] The real admin account can log in (don't rely only on a session
      that's already open in your browser)
- [ ] A recent backup exists (see `backup.md`)

## Before the Event

- [ ] `docker compose ps` — all services (`ctfd`, `db`, `cache`, `nginx`)
      are `Up`, `permissions` completed successfully
- [ ] CTFd itself loads over the real event URL, not just `localhost`
- [ ] All challenges are in the intended state (`visible`/`hidden`) —
      review Admin → Challenges, check the **Setup** column for `NO FLAG`
      / `NO DESCRIPTION` warnings on anything meant to go live
- [ ] Challenge files download and match what's expected
- [ ] Web/pwn challenge servers (if any) are reachable from a normal
      participant network, not just from the ops machine
- [ ] Flag submission works end-to-end: solve a real challenge with a test
      account and confirm the score updates
- [ ] Scoreboard reflects that test solve correctly, then decide whether to
      reset/hide that test account before going live
- [ ] Test user login/logout/register flow works
- [ ] Real admin login works (not just the session you're already in)
- [ ] Full backup completed and stored outside `platform/` (see
      `backup.md`, "before the event goes live")

## During the Event

- [ ] Periodically check server/container health (`docker compose ps`,
      `docker compose logs ctfd`)
- [ ] Watch for and respond to participant questions (Discord/whatever
      channel you use — not part of this codebase, but part of the job)
- [ ] Check Admin → Notifications if you need to post an announcement, and
      re-read it as a participant would before sending
- [ ] If a challenge is reported broken, verify from a clean participant
      account before changing anything — check the challenge's Setup
      warnings, its files, and (for hosted challenges) the challenge
      server's own logs
- [ ] Take periodic backups per the schedule in `backup.md`
- [ ] Log any real incident in `incident-log.md` as it happens, not
      afterward from memory

## After the Event

- [ ] Freeze the scoreboard (Admin → Config) before anything else, so
      final standings can't shift while you wrap up
- [ ] Confirm final scores/standings look correct — spot-check the top few
      places against the raw Submissions list
- [ ] Publish write-ups / solutions if planned
- [ ] Take the final backup (DB dump + uploads) and label it clearly as
      the post-event record — see `backup.md`
- [ ] Archive or export anything needed for certificates/reporting
- [ ] Send the participant survey/feedback form, if used
- [ ] Decide what happens to test accounts and any temporary QA data
      before the platform is reused for the next event
