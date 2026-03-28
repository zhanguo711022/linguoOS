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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS curriculum_progress(
              user_id TEXT,
              level_id TEXT,
              module_id TEXT,
              completed INTEGER,
              score REAL,
              updated_ts INTEGER,
              PRIMARY KEY (user_id, module_id)
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


def save_progress(user_id: str, level_id: str, module_id: str, completed: bool, score: float) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO curriculum_progress(
              user_id, level_id, module_id, completed, score, updated_ts
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, level_id, module_id, 1 if completed else 0, score, int(time.time())),
        )
        conn.commit()


def get_progress(user_id: str) -> dict:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT level_id, module_id, completed, score, updated_ts
            FROM curriculum_progress
            WHERE user_id=?
            """,
            (user_id,),
        ).fetchall()
    if not rows:
        return {\"level_id\": \"\", \"modules\": {}}
    latest = max(rows, key=lambda row: row[4])
    level_id = latest[0] or \"\"
    modules = {row[1]: float(row[3] or 0.0) for row in rows if row[1]}
    return {\"level_id\": level_id, \"modules\": modules}
