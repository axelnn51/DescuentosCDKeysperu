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
    "adorno colgante árbol", "pack cortinero", "porta reloj"
]

# Accesorios propensos a precios de lista falsos/inflados en marketplaces
MARKETPLACE_INFLATED_ITEMS = [
    "bolso", "cartera", "case", "funda", "soporte", "cable", "adaptador",
    "polo", "taza", "adorno", "joya", "collar", "pulsera", "aretes"
]

def is_valid_deal(deal: Deal) -> Tuple[bool, str]:
    """Evalúa si una oferta es de valor real, descartando chatarra, productos menores y descuentos falsos."""
    # Las promociones de cupones o 2x1 verificadas se aceptan
    if deal.deal_type in ("coupon", "2x1", "flash"):
        return True, "Cupón o promo verificada"

    title_lower = deal.title.lower()

    # 1. Filtro Anti-Basura (Verduras a granel, tornillos, repuestos menores)
    for junk in JUNK_KEYWORDS:
        if junk in title_lower:
            return False, f"Descartado por producto menor/chatarra: '{junk}'"

    # 2. Filtro de Precio Mínimo de Oferta (Nadie quiere alertas de cosas de 1 sol o 10 céntimos)
    if deal.discount_price < 12.0:
        return False, f"Precio de oferta insignificante (S/. {deal.discount_price:.2f} < S/. 12.00)"

    # 3. Filtro de Ahorro Real Mínimo
    if deal.savings < 20.0:
        return False, f"Ahorro insignificante (S/. {deal.savings:.2f} < S/. 20.00)"

    # 4. Detector de Descuentos Falsos / Inflados
    # Ejemplo: Productos que supuestamente costaban 20,000 o 100,000 millones y los venden a 80 soles
    if deal.original_price > 2500 and deal.discount_price < 120:
        return False, f"Descuento falso detectado: precio original inflado (S/. {deal.original_price} vs S/. {deal.discount_price})"

    if deal.discount_percent > 94:
        # Si un accesorio simple dice tener 95%+ de descuento y costar miles de soles, es falso
        for item in MARKETPLACE_INFLATED_ITEMS:
            if item in title_lower and deal.original_price > 1000:
                return False, f"Descuento inflado de seller en accesorio: '{item}'"

    return True, "Oferta válida y relevante"
