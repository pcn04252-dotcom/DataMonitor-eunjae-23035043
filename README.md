# DataMonitor

콘솔에서 저장된 데이터 상태를 조회할 수 있는 관리자 도구 PoC 프로젝트입니다.

- 언어: Python (`sqlite3` 표준 라이브러리)
- 상태: 구현 완료
- 상세 계획: [`PLAN.md`](./PLAN.md), 세션 참고 문서: [`CLAUDE.md`](./CLAUDE.md)

## 실행 방법

```
python -m src.seed   # 최초 1회, 데모 데이터 생성
python -m src.main   # 모니터링 콘솔 실행
```

콘솔에서 `[R]`을 입력하면 최신 데이터로 재조회/재렌더링하고, `[0]`을 입력하면 종료합니다.

## 테스트 방법

```
pip install -r requirements-dev.txt
pytest
```

## 검증한 것

- `pytest` 4개 테스트 통과 (조회/집계 함수, `:memory:` DB)
- DB 파일이 없을 때 안내 메시지를 출력하고 에러 없이 정상 종료(exit code 0)하는 것 확인
- `seed` → 조회 → `[R]` 새로고침 → `[0]` 종료 시나리오를 실제 입력으로 실행해 확인
