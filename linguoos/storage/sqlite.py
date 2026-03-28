import os
import sqlite3
import time

DB_PATH = os.getenv("LINGUO_DB_PATH", "linguoos/data/linguoos.db")


def _ensure_dir() -> None:
    d = os.path.dirname(DB_PATH) or "."
    os.makedirs(d, exist_ok=True)


def init_db() -> None:
    _ensure_dir()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              ts INTEGER,
              user_id TEXT,
              module_id TEXT,
              text TEXT,
              correct INTEGER
            )
            """
        )
        conn.commit()


def save_attempt(user_id: str, module_id: str, text: str, correct: bool) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO attempts(ts,user_id,module_id,text,correct) VALUES(?,?,?,?,?)",
            (int(time.time()), user_id, module_id, text, 1 if correct else 0),
        )
        conn.commit()


def recent_attempts(user_id: str | None, limit: int = 20):
    init_db()
    q = "SELECT ts,user_id,module_id,text,correct FROM attempts "
    p = []
    if user_id:
        q += "WHERE user_id=? "
        p.append(user_id)
    q += "ORDER BY id DESC LIMIT ?"
    p.append(limit)
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(q, tuple(p)).fetchall()
        return [
            {
                "ts": r[0],
                "user_id": r[1],
                "module_id": r[2],
                "text": r[3],
                "correct": bool(r[4]),
            }
            for r in rows
        ]


def clear_attempts(user_id: str | None) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        if user_id:
            conn.execute("DELETE FROM attempts WHERE user_id=?", (user_id,))
        else:
            conn.execute("DELETE FROM attempts")
        conn.commit()
