import sys

from src.db import get_connection

_DEMO_ITEMS = [
    ("실리콘 웨이퍼-8인치", 480),
    ("GaN 에피택셜-4인치", 220),
    ("SiC 파워기판-6인치", 30),
    ("산화막 웨이퍼-SiO2", 0),
    ("포토레지스트-PR7", 910),
]


def seed(conn) -> int:
    conn.executemany("INSERT INTO items (name, quantity) VALUES (?, ?)", _DEMO_ITEMS)
    conn.commit()
    return len(_DEMO_ITEMS)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    with get_connection() as conn:
        count = seed(conn)

    print(f"데모 데이터 {count}건을 생성했습니다.")


if __name__ == "__main__":
    main()
