# OSINT-02 Where Is This Writeup

## 문제 개요

사진 안의 명확한 간판과 주변 단서를 이용해 위치를 찾는다.

## 핵심 개념

입문 OSINT geolocation은 obscure한 추측이 아니라 눈에 보이는 텍스트, 랜드마크, 방향 정보를 정리하는 것에서 시작한다.

## 분석

사진에는 `UNKNOWN Tower`와 `Blue Harbor` 단서가 보인다. 제공된 mini map index에서 `UNKNOWN Tower`와 연결된 장소를 찾는다.

## 풀이

`mini-map-index.csv`에서 nearby clue가 `UNKNOWN Tower`인 행을 찾으면 `Blue Harbor Station`이다.

## Flag 획득

해당 행의 flag 값이 정답이다.

## 학습 포인트

사진 속 텍스트 단서는 지도 검색이나 색인 검색의 가장 쉬운 출발점이다.
