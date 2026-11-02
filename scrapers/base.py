from abc import ABC, abstractmethod
from typing import List
from models import Deal

class BaseScraper(ABC):
    @property
    @abstractmethod
    def store_name(self) -> str:
        pass

    @abstractmethod
    def fetch_deals(self, min_discount: float, max_items: int) -> List[Deal]:
        """Extrae ofertas de la tienda que superen el porcentaje mínimo de descuento."""
        pass
