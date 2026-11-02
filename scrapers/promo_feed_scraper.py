import re
from typing import List
from bs4 import BeautifulSoup
from models import Deal
from scrapers.base import BaseScraper

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

PROMO_CHANNELS = [
    ("El Datero Cuponero", "https://t.me/s/eldaterocuponero"),
]

class PromoFeedScraper(BaseScraper):
    def __init__(self):
        self._name = "Cupones y Promos Perú"

    @property
    def store_name(self) -> str:
        return self._name

    def fetch_deals(self, min_discount: float = 50.0, max_items: int = 20) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PE,es;q=0.9",
        }

        for source_name, url in PROMO_CHANNELS:
            try:
                resp = cffi_requests.get(url, impersonate="chrome124", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                messages = soup.select(".tgme_widget_message_wrap")

                # Tomar los últimos mensajes más recientes
                for m in reversed(messages[-25:]):
                    text_elem = m.select_one(".tgme_widget_message_text")
                    if not text_elem:
                        continue

                    full_text = text_elem.get_text(" ", strip=True)
                    if len(full_text) < 15:
                        continue

                    # Extraer enlace directo
                    link_elem = text_elem.select_one("a[href*='http']") or m.select_one("a[href*='http']")
                    target_url = link_elem["href"] if link_elem else url

                    # Extraer foto si tiene
                    image_url = None
                    photo_elem = m.select_one(".tgme_widget_message_photo_wrap")
                    if photo_elem:
                        style = photo_elem.get("style", "")
                        match = re.search(r"url\('([^']+)'\)", style)
                        if match:
                            image_url = match.group(1)

                    # Determinar tipo de oferta
                    is_2x1 = bool(re.search(r"2\s*x\s*1|2\s*unidades", full_text, re.I))
                    is_coupon = bool(re.search(r"cup[oó]n|c[oó]digo|rappi|pedidosya", full_text, re.I))

                    deal_type = "2x1" if is_2x1 else ("coupon" if is_coupon else "flash")

                    # Extraer precio si se menciona
                    price_match = re.search(r"S/\.?\s*([0-9]+(?:\.[0-9]{2})?)", full_text)
                    offer_price = float(price_match.group(1)) if price_match else 0.0
                    orig_price = offer_price * 2 if is_2x1 else (offer_price * 1.5 if offer_price > 0 else 0.0)

                    # Extraer título limpio (primeras 2 líneas o frase)
                    lines = [ln.strip() for ln in text_elem.stripped_strings if ln.strip()]
                    title = " ".join(lines[:3]) if lines else full_text[:90]

                    # Generar ID único por texto
                    pid = f"promo_{abs(hash(full_text))}"

                    deals.append(Deal(
                        store=f"Promo / Cupón ({source_name})",
                        product_id=pid,
                        title=title[:120],
                        url=target_url,
                        image_url=image_url,
                        original_price=orig_price,
                        discount_price=offer_price,
                        discount_percent=75.0 if is_2x1 else 50.0,
                        stock=1,
                        currency="S/.",
                        deal_type=deal_type,
                        description=full_text
                    ))

                    if len(deals) >= max_items:
                        break
            except Exception:
                continue

        return deals
