# MISC-03 Metadata Writeup

## 문제 개요

이미지 자체는 평범하지만 metadata에 단서가 있다.

## 핵심 개념

이미지 파일에는 작성자, 설명, 도구 정보 같은 metadata가 포함될 수 있다.

## 분석

`exiftool ordinary.png` 또는 metadata 확인 도구로 텍스트 필드를 확인한다.

## 풀이

PNG metadata의 description/comment 값을 읽는다.

## Flag 획득

metadata 안의 `UNKNOWN{...}` flag를 제출한다.

## 학습 포인트

겉으로 보이는 이미지뿐 아니라 파일 metadata도 분석 대상이다.
