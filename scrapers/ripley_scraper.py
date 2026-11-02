import json
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
    import urllib.request

RIPLEY_CATEGORIES = [
    "calzado",
    "tecnologia",
    "electrohogar",
    "deporte-y-aventura",
    "dormitorio",
    "belleza"
]

class RipleyScraper(BaseScraper):
    def __init__(self):
        self._name = "Ripley"
        self.base_url = "https://simple.ripley.com.pe"

    @property
    def store_name(self) -> str:
        return self._name

    def _slugify(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")

    def fetch_deals(self, min_discount: float = 75.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PE,es;q=0.9",
        }

        # Iterar por las categorías con mayores liquidaciones
        for cat in RIPLEY_CATEGORIES:
            if len(deals) >= max_items:
                break
            url = f"{self.base_url}/{cat}?orderBy=discount&page=1"
            try:
                resp = cffi_requests.get(url, impersonate="chrome124", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                script = soup.find("script", id="__NEXT_DATA__")
                if not script or not script.string:
                    continue

                data = json.loads(script.string)
                findability = data.get("props", {}).get("pageProps", {}).get("findabilityProps", {})
                products = findability.get("data", {}).get("products", [])

                # Mapa de URLs directas desde el HTML para mayor precisión
                link_map = {}
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    # Ripley links follow format: /slug-pid?...
                    match = re.search(r"/([^/]+)-([A-Za-z0-9]+)(\?.*)?$", href)
                    if match:
                        pid = match.group(2)
                        clean_href = href.split("?")[0]
                        link_map[pid] = clean_href if clean_href.startswith("http") else f"{self.base_url}{clean_href}"

                for p in products:
                    try:
                        pid = str(p.get("parentProductID") or p.get("sku") or "")
                        title = p.get("name", "").strip()
                        in_stock = p.get("inStock", True)
                        if not in_stock:
                            continue

                        # Precios
                        price = float(p.get("priceNumber") or 0)
                        orig_price = float(p.get("masterPriceNumber") or 0)
                        
                        # Si tiene precio ripley especial aún menor
                        ripley_price = p.get("ripleyPriceNumber")
                        if ripley_price and float(ripley_price) > 0:
                            price = float(ripley_price)

                        if orig_price <= 0 or price <= 0 or price >= orig_price:
                            continue

                        discount = round(((orig_price - price) / orig_price) * 100, 1)

                        if discount >= min_discount:
                            prod_url = link_map.get(pid)
                            if not prod_url:
                                prod_url = f"{self.base_url}/{self._slugify(title)}-{pid}"

                            img = p.get("primaryImage")
                            deals.append(Deal(
                                store=self.store_name,
                                product_id=f"ripley_{pid}",
                                title=title,
                                url=prod_url,
                                image_url=img,
                                original_price=orig_price,
                                discount_price=price,
                                discount_percent=discount,
                                stock=1,
                                currency="S/."
                            ))
                    except Exception:
                        continue
            except Exception:
                continue

        return deals
