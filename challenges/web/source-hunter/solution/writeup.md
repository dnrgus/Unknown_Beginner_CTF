# WEB-01 Source Hunter Writeup

## 문제 개요

첫 화면에는 Flag가 보이지 않지만, 서버가 내려준 HTML 안에 숨겨진 디버그 경로가 남아 있다.

## 핵심 개념

브라우저에 보이는 화면과 실제 HTML 소스는 다를 수 있다. DevTools나 페이지 소스 보기는 Web 입문에서 가장 먼저 확인해야 하는 관찰 도구다.

## 분석

메인 페이지 소스를 보면 다음과 같은 HTML 주석이 있다.

```html
<!-- TODO: remove debug route before launch: /debug-source-map-7f3a -->
```

## 풀이

브라우저에서 `/debug-source-map-7f3a`로 이동하거나 `curl`로 요청한다.

```bash
curl http://localhost:8101/debug-source-map-7f3a
```

## Flag 획득

응답 본문에 `UNKNOWN{view_source_is_a_superpower}`가 출력된다.

## 학습 포인트

화면에 보이지 않는 HTML 주석, 숨겨진 링크, 스크립트 경로도 서버가 보낸 정보다. 먼저 소스와 네트워크 요청을 관찰하자.
