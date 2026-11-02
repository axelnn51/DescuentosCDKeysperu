import sqlite3
import re
from datetime import datetime
from config import DB_PATH
from models import Deal
from typing import List, Tuple

def clean_title_for_dedup(title: str) -> str:
    """Normaliza un título para evitar duplicados entre distintas tiendas del mismo grupo."""
    text = title.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    # Palabras irrelevantes
    tokens = [w for w in text.split() if len(w) > 2 and w not in ("para", "con", "del", "las", "los", "por")]
    return " ".join(tokens[:8])

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notified_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            product_id TEXT NOT NULL,
            title TEXT,
            title_clean TEXT,
            url TEXT,
            original_price REAL,
            discount_price REAL,
            discount_percent REAL,
            deal_type TEXT DEFAULT 'discount',
            notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store, product_id)
        )
    """)
    cursor.execute("PRAGMA table_info(notified_deals)")
    cols = [r[1] for r in cursor.fetchall()]
    if "title_clean" not in cols:
        cursor.execute("ALTER TABLE notified_deals ADD COLUMN title_clean TEXT")
    if "deal_type" not in cols:
        cursor.execute("ALTER TABLE notified_deals ADD COLUMN deal_type TEXT DEFAULT 'discount'")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_store_pid ON notified_deals(store, product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title_clean ON notified_deals(title_clean)")
    conn.commit()
    conn.close()

def should_notify(deal: Deal) -> bool:
    """
    Retorna True si la oferta es verdaderamente nueva.
    Evita repetidos entre tiendas que venden el mismo producto (ej: Oechsle y Plaza Vea).
    """
    init_db()
    title_clean = clean_title_for_dedup(deal.title)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Comprobación exacta por ID en la misma tienda
    cursor.execute("""
        SELECT discount_price FROM notified_deals
        WHERE store = ? AND product_id = ?
    """, (deal.store, deal.product_id))
    row = cursor.fetchone()

    if row is not None:
        prev_price = row[0]
        conn.close()
        # Solo renotificar si el precio bajó significativamente más
        return deal.discount_price < prev_price - 2.0

    # 2. Comprobación cruzada entre tiendas distintas por título normalizado
    if title_clean:
        cursor.execute("""
            SELECT store, discount_price FROM notified_deals
            WHERE title_clean = ?
        """, (title_clean,))
        cross_row = cursor.fetchone()
        if cross_row is not None:
            conn.close()
            # Ya fue avisado en otra tienda; no repetir
            return False

    conn.close()
    return True

def record_notification(deal: Deal):
    """Guarda o actualiza la oferta notificada en la base de datos."""
    init_db()
    title_clean = clean_title_for_dedup(deal.title)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notified_deals (store, product_id, title, title_clean, url, original_price, discount_price, discount_percent, deal_type, notified_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(store, product_id) DO UPDATE SET
            discount_price = excluded.discount_price,
            discount_percent = excluded.discount_percent,
            notified_at = excluded.notified_at
    """, (
        deal.store,
        deal.product_id,
        deal.title,
        title_clean,
        deal.url,
        deal.original_price,
        deal.discount_price,
        deal.discount_percent,
        deal.deal_type,
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
