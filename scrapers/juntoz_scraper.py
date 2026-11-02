import re
from typing import List, Optional
from bs4 import BeautifulSoup
from models import Deal
from scrapers.base import BaseScraper

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

JUNTOZ_QUERIES = ["laptops", "celulares", "tecnologia", "zapatillas", "remate", "liquidaciones"]

class JuntozScraper(BaseScraper):
    def __init__(self):
        self._name = "Juntoz"
        self.base_url = "https://juntoz.com"

    @property
    def store_name(self) -> str:
        return self._name

    def _extract_prices(self, text: str):
        # Busca patrones de precios peruanos: S/. 4,699.00 o S/ 4699.00
        matches = re.findall(r"S/\.?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)", text)
        prices = []
        for m in matches:
            val_str = m.replace(",", "").strip()
            try:
                val = float(val_str)
                if val > 0:
                    prices.append(val)
            except ValueError:
                continue
        return prices

    def fetch_deals(self, min_discount: float = 75.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PE,es;q=0.9",
        }

        for q in JUNTOZ_QUERIES:
            if len(deals) >= max_items:
                break
            url = f"{self.base_url}/catalogo?keywords={q}"
            try:
                resp = cffi_requests.get(url, impersonate="chrome124", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                product_links = soup.find_all("a", href=re.compile(r"^/p/"))
                seen_urls = set()

                for a in product_links:
                    href = a.get("href", "")
                    if not href or href in seen_urls:
                        continue
                    seen_urls.add(href)

                    # Obtener tarjeta contenedora (subir 1-2 niveles)
                    parent = a
                    card = None
                    for _ in range(4):
                        parent = parent.parent
                        if not parent:
                            break
                        text = parent.get_text(" ", strip=True)
                        if "S/" in text:
                            card = parent
                            break

                    if not card:
                        continue

                    # Extraer precios
                    card_text = card.get_text(" ", strip=True)
                    prices = self._extract_prices(card_text)
                    if len(prices) < 2:
                        continue

                    orig_price = max(prices[0], prices[1])
                    offer_price = min(prices[0], prices[1])

                    if orig_price <= 0 or offer_price <= 0 or offer_price >= orig_price:
                        continue

                    discount = round(((orig_price - offer_price) / orig_price) * 100, 1)

                    if discount >= min_discount:
                        # Extraer título
                        title = ""
                        title_candidate = card.find(class_=re.compile(r"title|name|truncate", re.I))
                        if title_candidate:
                            title = title_candidate.get_text(strip=True)
                        if not title:
                            # Derivar del slug
                            slug = href.replace("/p/", "").split("-")[0:6]
                            title = " ".join(slug).title()

                        # Extraer imagen
                        img = card.find("img")
                        img_url = img.get("src") if img else None

                        full_url = f"{self.base_url}{href}"
                        pid = f"juntoz_{hash(href)}"

                        deals.append(Deal(
                            store=self.store_name,
                            product_id=pid,
                            title=title,
                            url=full_url,
                            image_url=img_url,
                            original_price=orig_price,
                            discount_price=offer_price,
                            discount_percent=discount,
                            stock=1,
                            currency="S/."
                        ))
            except Exception:
                continue

        return deals
