# CRYPTO-02 Base Adventure Writeup

## 문제 개요

문자열이 여러 encoding 단계를 거쳐 변환되어 있다.

## 핵심 개념

Encoding은 데이터를 표현하는 방식이지, key가 필요한 encryption이 아니다.

## 분석

처음 문자열은 Base64 문자 집합처럼 보인다. Base64로 한 번 풀면 hex 문자열이 나오고, hex를 bytes로 바꾸면 다시 Base64가 나온다.

## 풀이

Base64 decode → hex decode → Base64 decode 순서로 처리한다.

## Flag 획득

마지막 결과에서 `UNKNOWN{...}` flag를 얻는다.

## 학습 포인트

출력 형태를 관찰하면서 다음 decoding 단계를 결정할 수 있다.
