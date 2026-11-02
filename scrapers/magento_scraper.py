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

MAGENTO_STORES_CATALOG = {
    "lacuracao": {
        "name": "La Curacao",
        "base_url": "https://www.lacuracao.pe",
        "search_queries": ["remate", "outlet", "liquidacion"]
    },
    "efe": {
        "name": "Tiendas Efe",
        "base_url": "https://www.efe.com.pe",
        "search_queries": ["remate", "outlet", "liquidacion"]
    },
    "hiraoka": {
        "name": "Hiraoka",
        "base_url": "https://hiraoka.com.pe",
        "search_queries": ["remate", "outlet", "liquidacion"]
    }
}

class MagentoScraper(BaseScraper):
    def __init__(self, store_key: str):
        self.store_key = store_key
        info = MAGENTO_STORES_CATALOG.get(store_key, {})
        self._name = info.get("name", store_key.title())
        self.base_url = info.get("base_url", f"https://www.{store_key}.pe")
        self.queries = info.get("search_queries", ["remate", "outlet"])

    @property
    def store_name(self) -> str:
        return self._name

    def _clean_price(self, text: Optional[str]) -> float:
        if not text:
            return 0.0
        # Ej: "S/ 1,199.00" -> 1199.0
        clean = re.sub(r"[^\d.]", "", text.replace(",", ""))
        try:
            return float(clean)
        except ValueError:
            return 0.0

    def fetch_deals(self, min_discount: float = 75.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PE,es;q=0.9",
        }

        for q in self.queries:
            if len(deals) >= max_items:
                break
            url = f"{self.base_url}/catalogsearch/result/?q={q}"
            try:
                resp = cffi_requests.get(url, impersonate="chrome124", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select(".product-item-info, .product-item")

                for card in cards:
                    try:
                        title_elem = card.select_one(".product-item-link, .product-item-name a")
                        if not title_elem:
                            continue

                        title = title_elem.text.strip()
                        prod_url = title_elem.get("href", "")
                        if not prod_url:
                            continue

                        # Imagen
                        img_elem = card.select_one(".product-image-photo")
                        img_url = None
                        if img_elem:
                            img_url = img_elem.get("data-src") or img_elem.get("src")

                        # Precios en Magento
                        old_price_elem = card.select_one(".old-price .price, [data-price-type='oldPrice'] .price")
                        special_price_elem = card.select_one(".special-price .price, [data-price-type='finalPrice'] .price")
                        
                        orig_price = self._clean_price(old_price_elem.text if old_price_elem else None)
                        offer_price = self._clean_price(special_price_elem.text if special_price_elem else None)

                        if orig_price <= 0 or offer_price <= 0 or offer_price >= orig_price:
                            continue

                        discount = round(((orig_price - offer_price) / orig_price) * 100, 1)

                        if discount >= min_discount:
                            pid = f"{self.store_key}_{hash(prod_url)}"
                            deals.append(Deal(
                                store=self.store_name,
                                product_id=pid,
                                title=title,
                                url=prod_url,
                                image_url=img_url,
                                original_price=orig_price,
                                discount_price=offer_price,
                                discount_percent=discount,
                                stock=1,
                                currency="S/."
                            ))
                    except Exception:
                        continue
            except Exception:
                continue

        return deals
