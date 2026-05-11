import sqlite3

DB_NAME = "voters.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = connect()
    cursor = conn.cursor()

    # ================= VOTERS TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        voterid TEXT UNIQUE NOT NULL,
        aadhaar TEXT UNIQUE,
        dob TEXT,
        image_path TEXT,
        voted INTEGER DEFAULT 0
    )
    """)

    # ================= VOTES TABLE (FOR DASHBOARD COUNTING) =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voterid TEXT NOT NULL,
        candidate TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ================= AUTO INITIALIZE =================
init_db()