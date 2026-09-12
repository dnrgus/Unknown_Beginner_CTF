# OSINT-03 Developer Mistake Writeup

## 문제 개요

현재 저장소 파일에는 flag가 없지만, 과거 commit에 민감한 정보가 남아 있다.

## 핵심 개념

Git은 삭제된 내용도 history에 남길 수 있다. 현재 파일만 보는 것으로는 충분하지 않다.

## 분석

`git log`, `git show`, `git log --patch`를 사용해 과거 변경 내용을 확인한다.

## 풀이

제공된 repo에서 `git log --all --patch`를 실행하고 삭제된 secret 내용을 찾는다.

## Flag 획득

과거 commit diff에서 `UNKNOWN{...}` flag를 확인한다.

## 학습 포인트

비밀값을 commit했다가 삭제해도 git history에는 남을 수 있다.
