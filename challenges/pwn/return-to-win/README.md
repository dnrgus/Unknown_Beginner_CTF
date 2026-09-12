# PWN-03 Return to Win

- Category: Pwn
- Difficulty: Easy+
- Concept: ret2win
- Flag Format: `UNKNOWN{example_flag}`

## Description

The binary has a `win()` function, but normal execution never calls it. Redirect control flow to `win()`.

## Files

- `challenge/return-to-win.c`
