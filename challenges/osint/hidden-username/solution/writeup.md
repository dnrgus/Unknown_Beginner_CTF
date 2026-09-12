# OSINT-01 Hidden Username Writeup

## 문제 개요

가상 프로필과 archive 자료에서 같은 username을 추적한다.

## 핵심 개념

OSINT의 기본은 한 자료에서 찾은 식별자를 다른 자료에 연결해 보는 것이다.

## 분석

`profile.html`의 HTML 주석에 canonical username이 있다. Archive 목록에는 같은 이름의 텍스트 파일이 존재한다.

## 풀이

username `unknown_nova`를 확인하고 `archive/unknown_nova.txt`를 연다.

## Flag 획득

해당 파일에서 `UNKNOWN{...}` flag를 확인한다.

## 학습 포인트

닉네임, username, email prefix 같은 반복 식별자는 pivot의 출발점이 된다.
