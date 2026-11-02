import re
from typing import Tuple
from models import Deal

# Palabras clave de productos insignificantes, verduras a granel, ferretería menor o descartables
JUNK_KEYWORDS = [
    "calabaza", "zapallo", "cebolla", "zanahoria", "tomate", "verdura", "fruta",
    "lechuga", "limon", "papa ", "camote",
    "tornillo", "tarugo", "alcayata", "armella", "perno", "tuerca", "arandela",
    "clavo", "terminal lenteja", "soporte canopla", "cinta aislante", "cinta teflon",
    "cinta de doble contacto", "cinta malla", "lija", "cáncamo", "bornera",
    "tapa ciega", "caja de pase", "mascarilla de tela", "mascarilla quirurgica",
    "vela misionera", "adorno colgante", "pack cortinero", "porta reloj",
    "ambientador para auto", "bolsa de basura", "papel higienico"
]

def is_valid_deal(deal: Deal) -> Tuple[bool, str]:
    """
    Filtro estricto de calidad:
    Garantiza que SOLO pasen ofertas de alto impacto, productos legítimos de tiendas
    reconocidas y elimina precios artificialmente inflados por terceros en marketplaces.
    """
    title_lower = deal.title.lower()

    # 1. Filtro Anti-Basura (Verduras a granel, tornillos, repuestos menores)
    for junk in JUNK_KEYWORDS:
        if junk in title_lower:
            return False, f"Descartado por producto menor/chatarra: '{junk}'"

    # 2. Filtro de Precio Mínimo: Ignorar cosas menores a S/. 25.00
    if deal.discount_price < 25.0:
        return False, f"Precio de oferta insignificante (S/. {deal.discount_price:.2f} < S/. 25.00)"

    # 3. Filtro de Ahorro Real Mínimo: Al menos S/. 35.00 de ahorro en dinero real
    if deal.savings < 35.0:
        return False, f"Ahorro insignificante (S/. {deal.savings:.2f} < S/. 35.00)"

    # 4. Anti-Precios Inflados de Marketplace (Sellers que inflan 'Precio Antes' a 10k o 20k)
    # En el retail peruano, un descuento superior al 85% en productos de más de S/. 75 es casi 100% ficticio.
    if deal.discount_percent >= 85.0 and deal.discount_price >= 75.0:
        return False, f"Descuento ficticio inflado ({deal.discount_percent:.0f}% en S/. {deal.discount_price})"

    # Límites máximos creíbles de 'Precio Normal' por categoría de producto
    if any(k in title_lower for k in ["extractor", "licuadora", "batidora", "cafetera", "freidora", "espaguetera", "menaje", "olla"]) and deal.original_price > 1800:
        return False, f"Precio inflado en electrodoméstico/menaje: S/. {deal.original_price}"

    if any(k in title_lower for k in ["silla", "butaca", "mesa", "estante"]) and deal.original_price > 2500 and deal.discount_price < 600:
        return False, f"Precio inflado en mueble: S/. {deal.original_price}"

    if any(k in title_lower for k in ["audifono", "auricular", "earbuds", "buds", "tws", "handsfree"]) and deal.original_price > 1200:
        return False, f"Precio inflado en audífonos: S/. {deal.original_price}"

    if any(k in title_lower for k in ["soporte", "rack", "base", "funda", "case", "adaptador", "cargador", "cable"]) and deal.original_price > 500:
        return False, f"Precio inflado en accesorio: S/. {deal.original_price}"

    if any(k in title_lower for k in ["parlante", "torre", "altavoz"]) and deal.original_price > 7000:
        return False, f"Precio inflado en audio: S/. {deal.original_price}"

    if any(k in title_lower for k in ["tanga", "hilo", "lenceria", "truza", "vincha", "cumpleaños", "adorno", "bowl"]) and deal.original_price > 200:
        return False, f"Precio inflado en accesorio menor: S/. {deal.original_price}"

    if any(k in title_lower for k in ["luz", "foco", "lampara", "colgante"]) and deal.original_price > 500:
        return False, f"Precio inflado en iluminación: S/. {deal.original_price}"

    # Ratio de desproporción: Precio antes no puede ser más de 4.5 veces el precio de oferta si cuesta más de S/. 200
    if (deal.original_price / deal.discount_price) > 4.5 and deal.discount_price > 200:
        return False, f"Desproporción sospechosa de precio ({deal.original_price} vs {deal.discount_price})"

    # 5. Criterio de Aprobación según Tipo de Oferta
    if deal.is_historical_low or deal.deal_type == "historical_low":
        # Mínimos Históricos en tecnología y marcas: acepta menor porcentaje si el ahorro en dinero es alto
        if not ((deal.discount_percent >= 20.0 and deal.savings >= 120.0) or
                (deal.discount_percent >= 30.0 and deal.savings >= 60.0) or
                (deal.discount_percent >= 45.0 and deal.savings >= 40.0)):
            return False, f"Mínimo histórico con variación insuficiente ({deal.discount_percent:.0f}%, ahorro S/. {deal.savings:.0f})"
    else:
        # Liquidaciones directas de tienda: requiere al menos 50% de rebaja real
        if deal.discount_percent < 50.0:
            return False, f"Descuento menor al 50% ({deal.discount_percent:.0f}% OFF)"

    return True, "Oferta de alto impacto confirmada"
