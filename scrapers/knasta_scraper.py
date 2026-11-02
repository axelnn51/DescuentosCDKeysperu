import json
from typing import List
from bs4 import BeautifulSoup
from models import Deal
from scrapers.base import BaseScraper

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

KNASTA_FEEDS = [
    "https://knasta.pe/results?knastaday=true&order=percent",
    "https://knasta.pe/results?q=tecnologia&order=percent",
    "https://knasta.pe/results?q=laptops&order=percent",
    "https://knasta.pe/results?q=televisores&order=percent",
    "https://knasta.pe/results?q=celulares&order=percent",
    "https://knasta.pe/results?q=electrohogar&order=percent",
    "https://knasta.pe/results?q=zapatillas&order=percent",
]

class KnastaHistoricalScraper(BaseScraper):
    def __init__(self):
        self._name = "Histórico Knasta Perú"

    @property
    def store_name(self) -> str:
        return self._name

    def fetch_deals(self, min_discount: float = 30.0, max_items: int = 50) -> List[Deal]:
        deals: List[Deal] = []
        if not HAS_CURL_CFFI:
            return deals

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PE,es;q=0.9",
        }

        seen_urls = set()

        for feed_url in KNASTA_FEEDS:
            try:
                resp = cffi_requests.get(feed_url, impersonate="chrome124", headers=headers, timeout=12)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                script = soup.find("script", id="__NEXT_DATA__")
                if not script or not script.string:
                    continue

                data = json.loads(script.string)
                products = data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("products", [])

                for p in products:
                    try:
                        url = p.get("url")
                        if not url or url in seen_urls:
                            continue
                        seen_urls.add(url)

                        title = p.get("title", "").strip()
                        store = p.get("retail_label") or p.get("retail", "Tienda").title()
                        current_price = float(p.get("current_price") or 0)
                        last_price = float(p.get("last_variation_price") or p.get("price_internet") or 0)
                        best_hist = float(p.get("best_variation_price") or 0)
                        is_hist_low = bool(p.get("is_best_price", False))
                        
                        # Caída de precio registrada
                        percent_raw = p.get("percent")
                        percent_drop = abs(float(percent_raw)) if percent_raw is not None else 0.0

                        # Si last_price no está o es menor, inferir de percent
                        if last_price <= current_price and percent_drop > 0:
                            last_price = round(current_price / (1 - (percent_drop / 100)), 2)

                        if last_price <= current_price or current_price <= 0:
                            continue

                        discount_calc = round(((last_price - current_price) / last_price) * 100, 1)

                        # Si es mínimo histórico, aceptamos caídas a partir de 20%, sino el min_discount
                        threshold = 20.0 if is_hist_low else min_discount
                        if discount_calc >= threshold:
                            img = p.get("image") or p.get("thumbnail_image")
                            pid = f"knasta_{p.get('kid') or hash(url)}"

                            deal_type = "historical_low" if is_hist_low else "discount"

                            deals.append(Deal(
                                store=store,
                                product_id=pid,
                                title=title,
                                url=url,
                                image_url=img,
                                original_price=last_price,
                                discount_price=current_price,
                                discount_percent=discount_calc,
                                stock=1,
                                currency="S/.",
                                deal_type=deal_type,
                                is_historical_low=is_hist_low,
                                best_historical_price=best_hist if best_hist > 0 else current_price
                            ))

                            if len(deals) >= max_items:
                                break
                    except Exception:
                        continue
            except Exception:
                continue

        return deals
