import sys

from src.db import DB_PATH, db_exists, get_connection
from src.monitor import fetch_items, render


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    if not db_exists():
        print(f"DB 파일이 없습니다: {DB_PATH}")
        print("먼저 'python -m src.seed'를 실행해 데모 데이터를 생성하세요.")
        return

    with get_connection() as conn:
        render(fetch_items(conn))
        while True:
            choice = input("[R] 새로고침  [0] 종료\n선택 > ").strip()
            if choice == "0":
                break
            if choice.upper() == "R":
                render(fetch_items(conn))
            else:
                print("올바른 명령을 입력하세요.")


if __name__ == "__main__":
    main()
