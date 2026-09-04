import sqlite3

class PersistentMemory:
    DB_PATH = "app/storage/memory.db"

    @classmethod
    def initialize(cls):
        conn = sqlite3.connect(
            cls.DB_PATH
        )
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            user_id TEXT PRIMARY KEY,
            goal TEXT,
            weak_areas TEXT,
            vocabulary TEXT,
            progress INTEGER
        )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def save_user(
        cls,
        user_id,
        goal,
        weak_areas,
        vocabulary,
        progress
    ):
        conn = sqlite3.connect(
            cls.DB_PATH
        )
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO user_memory
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            goal,
            ",".join(weak_areas),
            ",".join(vocabulary),
            progress
        ))
        conn.commit()
        conn.close()
