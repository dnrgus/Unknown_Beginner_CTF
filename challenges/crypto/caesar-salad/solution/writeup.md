# CRYPTO-01 Caesar Salad Writeup

## 문제 개요

문제 파일에는 회전된 알파벳 문자열이 있다.

## 핵심 개념

Caesar cipher는 알파벳을 일정 칸 밀어 치환하는 방식이다.

## 분석

설명에 `rotated by 13`이 있으므로 ROT13을 적용한다. ROT13은 같은 연산을 한 번 더 적용하면 원문으로 돌아온다.

## 풀이

암호문 전체에 ROT13을 적용하고 `UNKNOWN{...}` 패턴을 찾는다.

## Flag 획득

복호화 결과에서 flag를 확인한다.

## 학습 포인트

Flag format은 복호화가 맞는지 확인하는 좋은 기준이 된다.
