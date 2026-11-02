import sqlite3
from datetime import datetime
from config import DB_PATH
from models import Deal
from typing import List, Tuple

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notified_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            product_id TEXT NOT NULL,
            title TEXT,
            url TEXT,
            original_price REAL,
            discount_price REAL,
            discount_percent REAL,
            notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store, product_id)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_store_pid ON notified_deals(store, product_id)")
    conn.commit()
    conn.close()

def should_notify(deal: Deal) -> bool:
    """Retorna True si la oferta es nueva o si el precio de oferta bajó aún más."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT discount_price FROM notified_deals
        WHERE store = ? AND product_id = ?
    """, (deal.store, deal.product_id))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return True
    
    prev_price = row[0]
    # Si bajó al menos 1 sol más, volvemos a avisar
    if deal.discount_price < prev_price - 0.5:
        return True
    
    return False

def record_notification(deal: Deal):
    """Guarda o actualiza la oferta notificada en la base de datos."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notified_deals (store, product_id, title, url, original_price, discount_price, discount_percent, notified_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(store, product_id) DO UPDATE SET
            discount_price = excluded.discount_price,
            discount_percent = excluded.discount_percent,
            notified_at = excluded.notified_at
    """, (
        deal.store,
        deal.product_id,
        deal.title,
        deal.url,
        deal.original_price,
        deal.discount_price,
        deal.discount_percent,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_stats() -> List[Tuple[str, int]]:
    """Devuelve el total de ofertas guardadas por tienda."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT store, COUNT(*) FROM notified_deals GROUP BY store ORDER BY COUNT(*) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
