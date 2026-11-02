# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-02 | Versión: v1.4.0 | Estado: Calidad Premium Verificada & Balance Multi-Tienda

## 1. 🚦 Estado Actual Inmediato
- 18 Fuentes Oficiales y Directas de Tiendas en Perú + Motor de Mínimos Históricos de Knasta Perú.
- **Filtro Anti-Precios Falsos**: Eliminados los vendedores de marketplace con precios ficticios inflados (ej: licuadoras o monitores supuestamente rebajados de S/. 16,000 a S/. 1,000). Filtro categórico y ratio máximo 4.5x.
- **Normalización y Deduplicación Inteligente**: Enriquecido `clean_title_for_dedup` eliminando variantes de color (`COLOR_STOPWORDS`) y deduplicando en memoria durante la recolección.
- **Distribución Balanceada por Tienda**: Máximo 3 ofertas por tienda por ciclo (15 alertas por ciclo en total) para garantizar variedad entre tecnología, hogar, moda y calzado.
- **Scoring Ponderado de Ofertas**: Prioriza el dinero real ahorrado en Soles (`savings * 0.4`), el porcentaje de rebaja y el bono de Mínimo Histórico verificado.
- Cero copias de canales de terceros. Todo original directamente desde tiendas y motores oficiales.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **Precios inflados de sellers (ej: Oster a S/. 16,990 o ViewSonic a S/. 10,089)**: Resuelto con topes categóricos plausibles en `filters.py` y detección de desproporción.
- **Duplicados del mismo producto o color**: Resuelto con filtrado de stopwords de color y set de títulos únicos por lote.
- **Monopolio de una sola tienda en el ciclo**: Resuelto con selector balanceado (máx. 3 alertas por tienda por ciclo).
- **Mínimos Históricos sin descuento (0% a 2%)**: Knasta ahora exige ahorro real mínimo de S/. 100 y al menos 20-25% de rebaja en tecnología/electro.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Scrapear canales de Telegram agregadores**: Descartado por requerimiento de originalidad.
- **Ordenar únicamente por mayor porcentaje bruto**: Descartado porque premiaba vendedores estafadores con descuentos falsos del 95%.

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [x] Push a GitHub: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- [ ] En Portainer: Hacer clic en "Pull and redeploy" en el Stack `descuentos`.

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Bot de Telegram: `@DsctCDKeysPerubot`
- Repositorio: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- Umbral general: 50% OFF (o 20-35% en Mínimos Históricos de alta gama con gran ahorro en Soles)
