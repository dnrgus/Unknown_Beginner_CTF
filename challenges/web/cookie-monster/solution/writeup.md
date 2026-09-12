# WEB-02 Cookie Monster Writeup

## 문제 개요

서비스는 사용자의 권한을 서버 세션이 아니라 브라우저 쿠키 `role` 값으로 판단한다.

## 핵심 개념

쿠키는 클라이언트가 저장하고 다시 서버로 보내는 값이다. 서명이나 서버 검증 없이 권한 정보를 쿠키에 그대로 넣으면 사용자가 값을 바꿀 수 있다.

## 분석

첫 방문 시 응답은 `role=guest` 쿠키를 설정한다. `/admin`은 이 쿠키 값이 `admin`인지 확인한다.

## 풀이

브라우저 DevTools의 Application/Cookies 탭에서 `role` 값을 `admin`으로 바꾼 뒤 `/admin`에 접속한다.

또는 Python requests로 쿠키를 지정한다.

```bash
python solution/solve.py http://localhost:8102
```

## Flag 획득

관리자 페이지가 `UNKNOWN{cookies_are_client_side}`를 출력한다.

## 학습 포인트

클라이언트가 보내는 쿠키, 파라미터, 헤더는 기본적으로 신뢰하면 안 된다. 권한 검사는 서버가 검증 가능한 방식으로 해야 한다.
