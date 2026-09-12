# CRYPTO-03 Reused XOR Writeup

## 문제 개요

flag가 하나의 byte key로 XOR되어 hex로 저장되어 있다.

## 핵심 개념

1-byte XOR key는 가능한 값이 0~255뿐이다. Flag prefix를 이용하면 정답을 쉽게 판별할 수 있다.

## 분석

hex를 bytes로 바꾼 뒤 모든 key 후보로 XOR한다. 결과에 `UNKNOWN{`가 포함되면 올바른 key다.

## 풀이

256개 key를 순회하며 복호화 결과를 검사한다.

## Flag 획득

올바른 key에서 `UNKNOWN{...}` flag가 나온다.

## 학습 포인트

무작정 큰 brute force는 피해야 하지만, 1-byte key처럼 작은 공간은 합리적인 검증 범위다.
