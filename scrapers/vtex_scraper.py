import json
import gzip
import urllib.request
import urllib.error
from typing import List, Dict
from models import Deal
from scrapers.base import BaseScraper

VTEX_STORES_CATALOG = {
    "plazavea": {"name": "Plaza Vea", "base_url": "https://www.plazavea.com.pe"},
    "oechsle": {"name": "Oechsle", "base_url": "https://www.oechsle.pe"},
    "metro": {"name": "Metro", "base_url": "https://www.metro.pe"},
    "wong": {"name": "Wong", "base_url": "https://www.wong.pe"},
    "promart": {"name": "Promart", "base_url": "https://www.promart.pe"},
    "coolbox": {"name": "Coolbox", "base_url": "https://www.coolbox.pe"},
    "footloose": {"name": "Footloose", "base_url": "https://www.footloose.pe"},
    "triathlon": {"name": "Triathlon Sport", "base_url": "https://www.triathlon.com.pe"},
    "casaideas": {"name": "Casaideas", "base_url": "https://www.casaideas.com.pe"},
    "sony": {"name": "Sony Store Perú", "base_url": "https://store.sony.com.pe"},
    "shopstar": {"name": "Shopstar", "base_url": "https://www.shopstar.pe"},
}

class VTEXScraper(BaseScraper):
    def __init__(self, store_key: str):
        self.store_key = store_key
        info = VTEX_STORES_CATALOG.get(store_key, {})
        self._name = info.get("name", store_key.title())
        self.base_url = info.get("base_url", f"https://www.{store_key}.pe")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "es-PE,es;q=0.9",
        }

    @property
    def store_name(self) -> str:
        return self._name

    def fetch_deals(self, min_discount: float = 75.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        limit = min(max_items, 50)
        url = f"{self.base_url}/api/catalog_system/pub/products/search?O=OrderByBestDiscountDESC&_from=0&_to={limit - 1}"

        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = resp.read()
                # Descomprimir gzip si viene comprimido
                if resp.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                data = json.loads(raw.decode("utf-8"))

                if not isinstance(data, list):
                    return deals

                for p in data:
                    try:
                        product_id = str(p.get("productId") or "")
                        title = p.get("productName", "").strip()
                        link = p.get("link", "")
                        if not link and p.get("linkText"):
                            link = f"{self.base_url}/{p.get('linkText')}/p"

                        items = p.get("items", [])
                        if not items:
                            continue

                        first_item = items[0]
                        # Obtener imagen
                        images = first_item.get("images", [])
                        image_url = images[0].get("imageUrl", "") if images else None

                        # Obtener oferta comercial
                        sellers = first_item.get("sellers", [])
                        if not sellers:
                            continue

                        comm = sellers[0].get("commertialOffer", {})
                        list_price = float(comm.get("ListPrice", 0))
                        price = float(comm.get("Price", 0))
                        stock = int(comm.get("AvailableQuantity", 0))

                        if list_price > 0 and price > 0 and list_price > price and stock > 0:
                            discount = round(((list_price - price) / list_price) * 100, 1)
                            if discount >= min_discount:
                                deals.append(Deal(
                                    store=self.store_name,
                                    product_id=product_id or f"{self.store_key}_{hash(link)}",
                                    title=title,
                                    url=link,
                                    image_url=image_url,
                                    original_price=list_price,
                                    discount_price=price,
                                    discount_percent=discount,
                                    stock=stock,
                                    currency="S/."
                                ))
                    except Exception:
                        continue
        except Exception as e:
            # print(f"[{self.store_name}] Error consultando ofertas: {e}")
            pass

        return deals

