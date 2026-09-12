# MISC-02 Magic Bytes Writeup

## 문제 개요

파일 확장자는 `.txt`지만 실제 파일 형식은 다르다.

## 핵심 개념

파일 형식은 확장자보다 magic bytes, 즉 파일 시작 시그니처를 보는 것이 정확하다.

## 분석

`file not_a_text.txt`를 실행하면 PNG 파일임을 알 수 있다.

## 풀이

파일을 PNG로 열어보거나 PNG 내부 텍스트 chunk를 확인한다.

## Flag 획득

PNG 파일 안의 `UNKNOWN{...}` flag를 확인한다.

## 학습 포인트

확장자는 사용자가 바꿀 수 있지만 magic bytes는 실제 파일 형식을 드러낸다.
