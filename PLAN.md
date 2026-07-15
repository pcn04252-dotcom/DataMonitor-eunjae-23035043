# PLAN: DataMonitor

> 이 문서는 구현이 진행됨에 따라 갱신되는 living document입니다. 실제 구현 중 발견된 이슈나 구조 변경 사항을 반영해 계속 업데이트합니다.

## 1. 목적

현재 저장된 데이터 상태를 콘솔에서 조회할 수 있는 관리자 도구를 검증하는 PoC.
`DataPersistence` PoC와 동일한 영속성 방식(SQLite)을 전제로 하되, 이 repo는 독립적으로 실행 가능해야 하므로 자체 데모용 DB를 준비한다.

## 2. 영속성 연동 방식

- SQLite 파일(`data/app.db`)에 연결하여 조회 전용으로 사용한다.
- "실시간 조회"는 백그라운드 스레드/스트리밍이 아니라, **사용자가 새로고침 명령을 입력할 때마다 즉시 재조회**하는 방식으로 구현한다 (콘솔 애플리케이션 특성상 polling on-demand 방식이 단순하고 충분함).

## 3. 데모 도메인: Item(품목)

`DataPersistence`와 동일한 스키마(`id`, `name`, `quantity`)를 그대로 사용해, 별도 DB 파일에서도 동일 구조로 동작함을 보여준다.

## 4. 폴더 구조

```
src/
  db.py            # 읽기 전용 DB 연결
  seed.py          # 단독 실행을 위한 데모 데이터 시딩 스크립트
  monitor.py       # 조회 + 콘솔 렌더링 + 새로고침 루프
  main.py          # 진입점
tests/
  test_monitor.py
```

## 5. 구현 단계

- [x] 1단계 - `db.py`: SQLite 연결 함수, 테이블 없을 시 자동 생성. `db_exists()`로 DB 파일 존재 여부를 별도 확인(있어야 진짜 데이터가 있는지 판단 가능, connection을 열면 파일이 자동 생성되어버리므로).
- [x] 2단계 - `seed.py`: 이 repo를 단독으로 시연할 수 있도록 데모 데이터 삽입 스크립트 (고정된 5건의 Item, PRD 예시 UI의 시료명 재사용).
- [x] 3단계 - `monitor.py`: `fetch_items`/`summarize`/`render` 함수 (조회 + 요약 통계 + 표 형태 콘솔 렌더링).
- [x] 4단계 - `main.py`: DB 없으면 안내 후 종료, 있으면 메뉴 루프 — `[R]` 입력 시 재조회 및 재렌더링, `[0]` 종료.
- [x] 5단계 - `tests/test_monitor.py`: 조회/집계 함수 단위 테스트 (`:memory:` DB 사용). 4개 테스트 통과.

## 6. 완료 기준 (Definition of Done)

- DB 파일이 없을 때 안내 메시지를 출력하고 정상 종료(에러 없이).
- `[R]` 입력 시 최신 데이터가 재조회되어 화면에 갱신 표시된다.
- 데이터 건수/요약 통계가 함께 표시된다.
- `pytest` 전체 통과.

## 7. 미결정/추후 논의 사항

- 실시간성 수준(폴링 주기 등)을 더 강화할지는 본 프로젝트(SampleOrderSystem) 요구사항을 보며 재검토.

## 8. 변경 이력

- 최초 작성
- `db_exists()` 함수 추가: `get_connection()`은 파일이 없으면 자동 생성해버리므로, DoD의 "DB 파일이 없을 때 안내 메시지" 요구사항을 만족하려면 connection을 열기 전에 파일 존재 여부를 먼저 확인해야 했음.
- 실제 시나리오(DB 없음 → 안내 후 정상 종료 / seed → 조회 → R 새로고침 → 0 종료) 수동 검증 완료.
- Harness 도입: `pyproject.toml`(pytest/ruff 설정), `requirements-dev.txt`(pytest, ruff), GitHub Actions CI(`.github/workflows/ci.yml`) 추가. `ruff check` 결과 이슈 없음.
