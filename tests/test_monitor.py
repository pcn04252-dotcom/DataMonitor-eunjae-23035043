from src.db import get_connection
from src.monitor import fetch_items, summarize


def test_fetch_items_returns_inserted_rows():
    with get_connection(":memory:") as conn:
        conn.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", ("품목A", 10))
        conn.commit()
        items = fetch_items(conn)
    assert len(items) == 1
    assert items[0]["name"] == "품목A"


def test_fetch_items_empty_when_no_rows():
    with get_connection(":memory:") as conn:
        items = fetch_items(conn)
    assert items == []


def test_summarize_counts_and_sums_quantity():
    with get_connection(":memory:") as conn:
        conn.executemany(
            "INSERT INTO items (name, quantity) VALUES (?, ?)",
            [("A", 10), ("B", 20)],
        )
        conn.commit()
        summary = summarize(fetch_items(conn))
    assert summary == {"count": 2, "total_quantity": 30}


def test_summarize_empty_items():
    assert summarize([]) == {"count": 0, "total_quantity": 0}
