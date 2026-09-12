# REV-01 Find the Password Writeup

## 문제 개요

바이너리가 비밀번호를 요구하고, 맞으면 flag를 출력한다.

## 핵심 개념

초보 reversing에서는 `strings`로 평문 문자열을 먼저 살펴보는 습관이 중요하다.

## 분석

`strings find-the-password`를 실행하면 `blue_keycard`라는 비밀번호 후보를 찾을 수 있다.

## 풀이

바이너리를 실행하고 `blue_keycard`를 입력한다.

## Flag 획득

정답을 입력하면 프로그램이 내부에서 flag를 복호화해 출력한다.

## 학습 포인트

평문 비밀번호는 바이너리 안에서 쉽게 발견된다.
