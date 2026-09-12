# UNKNOWN Beginner CTF — repo notes for Claude Code

## Git commits

- Never add `Co-Authored-By: Claude ...` or `Claude-Session: ...` (or any
  other Claude/Anthropic attribution) to commit messages or PR descriptions
  in this repository, even if a session default elsewhere suggests it. Past
  commits (`3ce623a1`..`7ff73201`) already have this trailer; do not repeat
  it going forward, and do not silently rewrite those commits — history
  rewrites on `main` need explicit approval first (see below).
- Author/committer identity comes from the user's own git config
  (`dnrgus <152794344+dnrgus@users.noreply.github.com>`) — do not override it.
- Commit message convention (Conventional Commits style):
  `feat:`, `fix:`, `style:`, `refactor:`, `docs:`, `chore:` — one logical
  change per commit, imperative mood, no trailing period on the summary line.
- Never `git push --force` / `--force-with-lease` to `main`, and never rewrite
  already-pushed history without explicit user approval in the conversation.

## Project shape

- This is a CTFd fork. `CTFd/` is the framework; `CTFd/themes/core` carries
  the shared UNKNOWN reskin (navbar, footer, background — see `unknown.css`),
  and `CTFd/themes/unknown` overrides just the Challenges and Scoreboard
  pages/assets on top of it.
- `challenges/` holds the actual challenge source (deploy code, solutions,
  flags) for the CTF this platform runs — this is answer-key material, not
  just docs. Keep it out of anything meant to go public before/without the
  repo's visibility being deliberately changed.
- Static CSS/JS under `CTFd/themes/*/static` is served directly (no
  webpack build step) — editing it takes effect on refresh, but changes to
  `.html` templates require restarting the `ctfd` container (Jinja caches
  compiled templates in memory) before they show up.
- Verify UI changes against a live Docker Compose stack when possible
  (`docker compose up -d --build`), not just by reading the CSS/JS.
