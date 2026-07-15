import sqlite3


def fetch_items(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT id, name, quantity FROM items ORDER BY id").fetchall()


def summarize(items: list[sqlite3.Row]) -> dict:
    return {
        "count": len(items),
        "total_quantity": sum(item["quantity"] for item in items),
    }


def render(items: list[sqlite3.Row]) -> None:
    summary = summarize(items)
    print("=" * 40)
    print(f"등록 품목 {summary['count']}종   총 재고 {summary['total_quantity']} ea")
    print("=" * 40)
    if not items:
        print("등록된 품목이 없습니다.")
        return
    print(f"{'ID':<4}{'이름':<20}{'재고'}")
    for item in items:
        print(f"{item['id']:<4}{item['name']:<20}{item['quantity']} ea")
