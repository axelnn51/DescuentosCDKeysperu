from typing import List
from scrapers.base import BaseScraper
from scrapers.vtex_scraper import VTEXScraper, VTEX_STORES_CATALOG
from scrapers.ripley_scraper import RipleyScraper
from scrapers.falabella_scraper import FalabellaScraper

def get_scrapers(enabled_keys: List[str]) -> List[BaseScraper]:
    scrapers: List[BaseScraper] = []
    
    for key in enabled_keys:
        k = key.lower().strip()
        if k in VTEX_STORES_CATALOG:
            scrapers.append(VTEXScraper(k))
        elif k == "ripley":
            scrapers.append(RipleyScraper())
        elif k == "falabella":
            scrapers.append(FalabellaScraper())

    return scrapers
