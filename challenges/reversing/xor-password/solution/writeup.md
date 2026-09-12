# REV-03 XOR Password Writeup

## 문제 개요

비밀번호가 평문이 아니라 XOR된 바이트 배열로 저장되어 있다.

## 핵심 개념

XOR는 같은 key로 다시 XOR하면 원래 값으로 돌아온다.

## 분석

바이너리의 배열과 `decode()` 함수를 보면 모든 바이트가 `0x5a`와 XOR되는 것을 알 수 있다.

## 풀이

encoded password 배열의 각 값을 `0x5a`와 XOR하면 `Lor_hunter`가 나온다. 이 값을 프로그램에 입력한다.

## Flag 획득

정답 비밀번호를 입력하면 flag 배열도 복호화되어 `UNKNOWN{...}`가 출력된다.

## 학습 포인트

고정 key XOR는 연산을 역으로 적용해 쉽게 복구할 수 있다.
