import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cards.db"

def ensureDatabaseExists():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id TEXT PRIMARY KEY NOT NULL
            )
        """)

def addCard(card_id: str):
    ensureDatabaseExists()
    if not card_id:
        raise ValueError("Niepoprawne Id karty!")

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("INSERT OR IGNORE INTO cards(card_id) VALUES (?)", (card_id,))
        return cur.rowcount == 1

def cardExists(card_id: str):
    ensureDatabaseExists()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT 1 FROM cards WHERE card_id = ? LIMIT 1", (card_id,))
        return cur.fetchone() is not None

def listCards():
    ensureDatabaseExists()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT card_id FROM cards ORDER BY card_id")
        return [row[0] for row in cur.fetchall()]


def deleteCard(card_id: str):
    ensureDatabaseExists()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM cards WHERE card_id = ?", (card_id,))
        return cur.rowcount == 1