import re
from typing import Tuple
from models import Deal

# Palabras clave de productos insignificantes, verduras a granel o ferretería menor
JUNK_KEYWORDS = [
    "calabaza", "zapallo", "cebolla", "zanahoria", "tomate", "verdura", "fruta",
    "tornillo", "tarugo", "alcayata", "armella", "perno", "tuerca", "arandela",
    "clavo", "terminal lenteja", "soporte canopla", "cinta aislante", "cinta teflon",
    "cinta de doble contacto", "cinta malla", "lija", "cáncamo", "bornera",
    "tapa ciega", "caja de pase", "mascarilla de tela", "vela misionera",
    "adorno colgante árbol", "pack cortinero"
]

# Accesorios propensos a precios de lista falsos/inflados en marketplaces
MARKETPLACE_INFLATED_ITEMS = [
    "bolso", "cartera", "case", "funda", "soporte", "cable", "adaptador",
    "taza", "adorno", "joya", "collar", "pulsera", "aretes"
]

def is_valid_deal(deal: Deal) -> Tuple[bool, str]:
    """Evalúa si una oferta es de valor real, descartando chatarra, productos menores y descuentos falsos."""
    title_lower = deal.title.lower()

    # 1. Filtro Anti-Basura (Verduras a granel, tornillos, repuestos menores)
    for junk in JUNK_KEYWORDS:
        if junk in title_lower:
            return False, f"Descartado por producto menor/chatarra: '{junk}'"

    # Si es Mínimo Histórico Real
    if deal.is_historical_low or deal.deal_type == "historical_low":
        if deal.discount_price < 20.0:
            return False, f"Precio demasiado bajo para mínimo histórico (S/. {deal.discount_price})"
        if deal.savings < 20.0 and deal.discount_percent < 15.0:
            return False, f"Ahorro insignificante en histórico (S/. {deal.savings})"
        return True, "Mínimo histórico confirmado y relevante"

    # 2. Filtro de Precio Mínimo de Oferta para liquidaciones generales
    if deal.discount_price < 15.0:
        return False, f"Precio de oferta insignificante (S/. {deal.discount_price:.2f} < S/. 15.00)"

    # 3. Filtro de Ahorro Real Mínimo
    if deal.savings < 25.0:
        return False, f"Ahorro insignificante (S/. {deal.savings:.2f} < S/. 25.00)"

    # 4. Detector de Descuentos Falsos / Inflados
    if deal.original_price > 2500 and deal.discount_price < 120:
        return False, f"Descuento falso detectado: precio original inflado (S/. {deal.original_price} vs S/. {deal.discount_price})"

    if deal.discount_percent > 94:
        for item in MARKETPLACE_INFLATED_ITEMS:
            if item in title_lower and deal.original_price > 1000:
                return False, f"Descuento inflado de seller en accesorio: '{item}'"

    return True, "Oferta válida y relevante"
