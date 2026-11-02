#!/usr/bin/env python3
"""
=============================================================
  SPY DE REBAJAS PERÚ - CAZADOR DE DESCUENTOS >= 75%
  Monitorea las principales tiendas del Perú y envía alertas
  en tiempo real a tu bot o canal de Telegram.
=============================================================
"""

import sys
import time
import argparse
from datetime import datetime

# Garantizar compatibilidad UTF-8 en consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    MIN_DISCOUNT_PERCENT,
    SCAN_INTERVAL_MINUTES,
    MAX_ITEMS_PER_STORE,
    ENABLED_STORES
)
from db import init_db, should_notify, record_notification, get_stats
from scrapers import get_scrapers
from telegram_notifier import TelegramNotifier
from filters import is_valid_deal

# Límite de alertas máximas por ciclo para balancear variedad y servidor
MAX_ALERTS_PER_CYCLE = 15

def print_banner():
    print(r"""
=============================================================
  🇵🇪  SPY DE REBAJAS PERÚ - BOT DE LIQUIDACIONES  🇵🇪
  Filtro actual: Rebajas y Mínimos Históricos en Tiendas Perú
=============================================================
""")

def run_scan(min_discount: float, max_items: int, dry_run: bool = False, store_filter: str = None) -> int:
    init_db()
    notifier = TelegramNotifier()

    stores_to_run = [store_filter.lower()] if store_filter else ENABLED_STORES
    scrapers = get_scrapers(stores_to_run)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando escaneo en {len(scrapers)} fuentes oficiales...")
    print(f"🎯 Umbral de descuento: >= {min_discount}% | Modo: {'DRY RUN (Solo prueba)' if dry_run else 'EN VIVO'}\n")

    candidates = []

    for scraper in scrapers:
        print(f"🔍 Consultando {scraper.store_name}...", end=" ", flush=True)
        try:
            deals = scraper.fetch_deals(min_discount=min_discount, max_items=max_items)
            print(f"-> {len(deals)} items leídos")

            for deal in deals:
                valid, reason = is_valid_deal(deal)
                if not valid:
                    continue

                if should_notify(deal):
                    candidates.append(deal)
        except Exception as e:
            print(f"-> Error: {e}")

    # Ordenar candidatos: primero MÍNIMOS HISTÓRICOS, luego mayor ahorro en dinero real
    candidates.sort(key=lambda d: (1 if d.is_historical_low else 0, d.savings), reverse=True)

    print(f"\n📊 Total de ofertas relevantes no notificadas: {len(candidates)}")
    selected_deals = candidates[:MAX_ALERTS_PER_CYCLE]

    total_notified = 0
    for deal in selected_deals:
        if deal.is_historical_low or deal.deal_type == "historical_low":
            tipo = "📉 [MÍNIMO HISTÓRICO]"
        else:
            tipo = f"🔥 [{deal.discount_percent:.0f}% OFF]"
        print(f"   {tipo} {deal.store} | S/. {deal.discount_price:,.2f} (Antes: S/. {deal.original_price:,.2f})")
        print(f"      {deal.title[:65]}")
        print(f"      🔗 {deal.url}")

        if not dry_run:
            sent = notifier.send_deal(deal)
            if sent or not notifier.is_configured():
                record_notification(deal)
                total_notified += 1
        else:
            total_notified += 1

    print("\n" + "=" * 60)
    print(f"🏁 Resumen: {len(candidates)} candidatas | {total_notified} enviadas a Telegram (Límite: {MAX_ALERTS_PER_CYCLE}/ciclo)")
    if not notifier.is_configured() and not dry_run:
        print("💡 Configura TELEGRAM_CHAT_ID para recibir los mensajes en tu chat privado.")
    print("=" * 60 + "\n")
    return total_notified

def run_daemon(min_discount: float, max_items: int, interval_mins: int):
    print_banner()
    print(f"⚙️ Modo demonio activado. Se ejecutará cada {interval_mins} minutos.")
    print("Presiona Ctrl + C para detener el bot.\n")

    while True:
        try:
            run_scan(min_discount=min_discount, max_items=max_items, dry_run=False)
            print(f"💤 Esperando {interval_mins} minutos para el próximo escaneo...\n")
            time.sleep(interval_mins * 60)
        except KeyboardInterrupt:
            print("\n🛑 Monitor de rebajas detenido por el usuario.")
            break
        except Exception as e:
            print(f"⚠️ Error imprevisto en ciclo: {e}. Reintentando en 60 segundos...")
            time.sleep(60)

def main():
    parser = argparse.ArgumentParser(description="Spy de Rebajas Perú - Alertas Telegram >= 75% OFF")
    parser.add_argument("--scan-once", action="store_true", help="Ejecutar un solo escaneo ahora mismo")
    parser.add_argument("--dry-run", action="store_true", help="Buscar ofertas e imprimir en consola sin enviar a Telegram")
    parser.add_argument("--daemon", action="store_true", help="Ejecutar en bucle continuo de monitoreo")
    parser.add_argument("--test-telegram", action="store_true", help="Probar el token y chat ID de Telegram")
    parser.add_argument("--get-chat-id", action="store_true", help="Detectar automáticamente tu chat_id desde Telegram")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadísticas de ofertas registradas")
    parser.add_argument("--min-discount", type=float, default=MIN_DISCOUNT_PERCENT, help="Porcentaje mínimo de descuento (ej: 75)")
    parser.add_argument("--max-items", type=int, default=MAX_ITEMS_PER_STORE, help="Máximo de productos por tienda")
    parser.add_argument("--interval", type=int, default=SCAN_INTERVAL_MINUTES, help="Intervalo en minutos para modo daemon")
    parser.add_argument("--store", type=str, default=None, help="Escanear solo una tienda específica (ej: oechsle, plazavea)")

    args = parser.parse_args()

    if args.get_chat_id:
        notifier = TelegramNotifier()
        cid, msg = notifier.auto_detect_chat_id()
        print(f"[{'EXITO' if cid else 'INFO'}] {msg}")
        if cid:
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    content = f.read()
                if "TELEGRAM_CHAT_ID=" in content:
                    lines = []
                    for line in content.splitlines():
                        if line.startswith("TELEGRAM_CHAT_ID="):
                            lines.append(f"TELEGRAM_CHAT_ID={cid}")
                        else:
                            lines.append(line)
                    with open(".env", "w", encoding="utf-8") as f:
                        f.write("\n".join(lines) + "\n")
                    print(f"💾 Guardado TELEGRAM_CHAT_ID={cid} en tu archivo .env automáticamente!")
            except Exception as e:
                print(f"⚠️ Guarda este ID manualmente: TELEGRAM_CHAT_ID={cid}")
        sys.exit(0 if cid else 1)

    if args.test_telegram:
        notifier = TelegramNotifier()
        ok, msg = notifier.test_connection()
        print(f"[{'EXITO' if ok else 'ERROR'}] {msg}")
        sys.exit(0 if ok else 1)

    if args.stats:
        stats = get_stats()
        print("\n📊 ESTADÍSTICAS DE REBAJAS NOTIFICADAS:")
        if not stats:
            print("Aún no hay ofertas registradas en la base de datos.")
        else:
            for store, count in stats:
                print(f"  * {store}: {count} ofertas")
        sys.exit(0)

    if args.daemon:
        run_daemon(min_discount=args.min_discount, max_items=args.max_items, interval_mins=args.interval)
    else:
        print_banner()
        run_scan(min_discount=args.min_discount, max_items=args.max_items, dry_run=args.dry_run, store_filter=args.store)

if __name__ == "__main__":
    main()
