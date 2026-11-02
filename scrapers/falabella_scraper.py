import json
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

FALABELLA_QUERIES = [
    "liquidaciones",
    "remate",
    "outlet"
]

class FalabellaScraper(BaseScraper):
    def __init__(self):
        self._name = "Falabella"
        self.base_url = "https://www.falabella.com.pe"

    @property
    def store_name(self) -> str:
        return self._name

    def _parse_price_str(self, val: any) -> float:
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, list) and val:
            val = val[0]
        s = str(val or "").replace("S/", "").replace("S/.", "").replace("$", "").replace(",", "").strip()
        try:
            return float(s)
        except ValueError:
            return 0.0

    def fetch_deals(self, min_discount: float = 75.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "Accept-Language": "es-PE,es;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

        for q in FALABELLA_QUERIES:
            if len(deals) >= max_items:
                break
            url = f"{self.base_url}/falabella-pe/search?Ntt={q}"
            try:
                resp = cffi_requests.get(url, impersonate="chrome", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                script = soup.find("script", id="__NEXT_DATA__")
                if not script or not script.string:
                    continue

                data = json.loads(script.string)
                results = data.get("props", {}).get("pageProps", {}).get("results", [])

                for r in results:
                    try:
                        pid = str(r.get("productId") or r.get("skuId") or "")
                        title = r.get("displayName", "").strip()
                        prod_url = r.get("url", "")
                        if prod_url and not prod_url.startswith("http"):
                            prod_url = f"{self.base_url}{prod_url}"

                        # Extraer imagen
                        images = r.get("mediaUrls", [])
                        image_url = images[0] if images else None

                        # Extraer precios
                        prices = r.get("prices", [])
                        normal_price = 0.0
                        offer_price = 0.0

                        for p in prices:
                            p_type = p.get("type", "")
                            p_raw = p.get("price")
                            val = self._parse_price_str(p_raw)
                            if p_type == "normalPrice" and val > 0:
                                normal_price = val
                            elif p_type in ("eventPrice", "internetPrice", "offerPrice") and val > 0:
                                offer_price = val

                        # Si solo hay un precio normal y otro no clasificado
                        if offer_price == 0.0 and len(prices) >= 2:
                            offer_price = self._parse_price_str(prices[0].get("price"))
                            normal_price = self._parse_price_str(prices[1].get("price"))

                        if normal_price <= 0 or offer_price <= 0 or offer_price >= normal_price:
                            continue

                        discount = round(((normal_price - offer_price) / normal_price) * 100, 1)

                        if discount >= min_discount:
                            deals.append(Deal(
                                store=self.store_name,
                                product_id=f"falabella_{pid}",
                                title=title,
                                url=prod_url,
                                image_url=image_url,
                                original_price=normal_price,
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

