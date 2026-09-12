# WEB-03 Baby SQL

- Category: Web
- Difficulty: Easy+
- Description: A tiny login form talks directly to SQL. Bypass authentication with a classic beginner payload.
- Files: Service only
- Connection: http://localhost:8103
- Flag Format: `UNKNOWN{example_flag}`

## Hints

1. The login form builds a SQL query from your input.
2. Try a payload that makes the WHERE condition always true, such as `' OR '1'='1' --`.
