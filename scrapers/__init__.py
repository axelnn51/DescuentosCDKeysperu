from typing import List
from scrapers.base import BaseScraper
from scrapers.vtex_scraper import VTEXScraper, VTEX_STORES_CATALOG
from scrapers.magento_scraper import MagentoScraper, MAGENTO_STORES_CATALOG
from scrapers.juntoz_scraper import JuntozScraper
from scrapers.ripley_scraper import RipleyScraper
from scrapers.falabella_scraper import FalabellaScraper
from scrapers.promo_feed_scraper import PromoFeedScraper

def get_scrapers(enabled_keys: List[str]) -> List[BaseScraper]:
    scrapers: List[BaseScraper] = []
    
    for key in enabled_keys:
        k = key.lower().strip()
        if k in VTEX_STORES_CATALOG:
            scrapers.append(VTEXScraper(k))
        elif k in MAGENTO_STORES_CATALOG:
            scrapers.append(MagentoScraper(k))
        elif k == "juntoz":
            scrapers.append(JuntozScraper())
        elif k == "ripley":
            scrapers.append(RipleyScraper())
        elif k == "falabella":
            scrapers.append(FalabellaScraper())
        elif k in ("cupones", "promos", "ofertas"):
            scrapers.append(PromoFeedScraper())

    # Siempre incluir cupones y promociones 2x1 si no están explicitamente
    has_cupones = any(isinstance(s, PromoFeedScraper) for s in scrapers)
    if not has_cupones:
        scrapers.append(PromoFeedScraper())

    return scrapers
