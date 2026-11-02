from dataclasses import dataclass
from typing import Optional

@dataclass
class Deal:
    store: str
    product_id: str
    title: str
    url: str
    image_url: Optional[str]
    original_price: float
    discount_price: float
    discount_percent: float
    stock: int = 1
    currency: str = "S/."
    deal_type: str = "discount" # "discount", "historical_low"
    description: Optional[str] = None
    is_historical_low: bool = False
    best_historical_price: Optional[float] = None

    @property
    def savings(self) -> float:
        return round(self.original_price - self.discount_price, 2)
