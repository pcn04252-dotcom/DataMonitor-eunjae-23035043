# CLAUDE.md

> 이 문서는 구현이 진행됨에 따라 갱신되는 living document입니다. 새 세션에서 이 repo를 열었을 때 아래 내용만으로 작업을 이어갈 수 있어야 합니다.

## 프로젝트 개요

콘솔에서 저장된 데이터를 조회하는 관리자(모니터링) 도구 PoC. 상세 계획은 `PLAN.md` 참고.

## 기술 스택

- Python 3.x + `sqlite3` (표준 라이브러리, 외부 의존성 없음)
- 테스트: `pytest`

## 폴더 구조

```
src/db.py         # 읽기 전용 DB 연결
src/seed.py       # 단독 실행용 데모 데이터 시딩
src/monitor.py    # 조회 + 렌더링
src/main.py       # 메뉴 루프 진입점
tests/
data/app.db       # 실제 데이터 (git 추적 제외)
```

## 실행 방법

```
python -m src.seed   # 최초 1회, 데모 데이터 생성
python -m src.main   # 모니터링 콘솔 실행
```

## 테스트 방법

```
pytest
```

## 코드 컨벤션

- `monitor.py`는 조회(SELECT) 전용이며 데이터를 변경하는 쿼리를 포함하지 않는다.
- 새로고침은 사용자 입력 트리거 방식(polling on-demand)으로 구현하고, 별도 스레드/타이머를 사용하지 않는다.
- 타입 힌트를 사용한다.

## 주의사항

- `data/app.db`는 `.gitignore`에 포함되어 커밋되지 않으므로, 이 repo만 클론해도 동작하도록 `seed.py`로 자체 데모 데이터를 만들 수 있어야 한다.
- 스키마는 `DataPersistence` repo와 동일한 설계 방향(Item: id/name/quantity)을 따르되, 코드/DB 파일을 직접 공유하지는 않는다.
