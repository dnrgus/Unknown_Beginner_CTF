# WEB-03 Baby SQL Writeup

## 문제 개요

로그인 폼의 입력값이 SQL 문자열에 그대로 들어간다. 이 때문에 사용자는 SQL 문법을 입력해 인증 조건을 바꿀 수 있다.

## 핵심 개념

SQL Injection은 사용자 입력이 쿼리 구조와 분리되지 않을 때 발생한다. 입문 단계에서는 WHERE 조건을 항상 참으로 만드는 인증 우회부터 이해하면 된다.

## 분석

서버는 다음과 같은 쿼리를 만든다.

```sql
SELECT username FROM users WHERE username = '<username>' AND password = '<password>'
```

username에 `' OR '1'='1' --`를 넣으면 뒤의 password 조건이 주석 처리되고, 조건이 항상 참이 된다.

## 풀이

폼에 다음 값을 입력한다.

- username: `' OR '1'='1' --`
- password: 아무 값

또는 자동 풀이를 실행한다.

```bash
python solution/solve.py http://localhost:8103
```

## Flag 획득

로그인이 우회되면 `UNKNOWN{baby_sqli_login_bypass}`가 출력된다.

## 학습 포인트

SQL 문자열을 직접 이어 붙이지 말고 prepared statement/parameterized query를 사용해야 한다.
