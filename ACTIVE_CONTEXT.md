# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-02 | Versión: v1.2.0 | Estado: Operativo, Filtrado Inteligente & Cupones

## 1. 🚦 Estado Actual Inmediato
- 17 Tiendas y Marketplaces + Módulo de Cupones en vivo (Rappi, PedidosYa, Promos 2x1 como Xiaomi Power Bank).
- Filtro inteligente anti-chatarra: Descarte automático de verduras a granel, tornillería menor y productos de centavos.
- Detector de precios inflados/falsos de sellers de marketplace (sanity check en precios y porcentajes).
- Deduplicación cruzada global (Cross-Store): Evita que el mismo producto se repita entre tiendas del mismo grupo (Oechsle, Plaza Vea, Shopstar).
- Control de flujo y throttling: Máximo 6 ofertas top por ciclo para no ahogar Telegram ni el servidor.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **Saturación y Spam de Productos Menores**: Solucionado con `filters.py` (blacklist de chatarra, precio mínimo de oferta S/. 12, ahorro mínimo real S/. 20).
- **Repetición entre tiendas hermanas (Intercorp/VTEX)**: Solucionado en `db.py` con `title_clean` deduplicando productos idénticos en distintas webs.
- **Precios Inflados de Sellers**: Solucionado detectando ratios irreales (> 18x en accesorios comunes).
- **Portainer "env file .env not found"**: Resuelto eliminando `env_file` y usando variables directas en `docker-compose.yml`.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Filtro matemático ciego sin validación de categoría**: Genera spam de calabazas y tornillos. Prohibido omitir `is_valid_deal()`.

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [x] Push a GitHub: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- [ ] En Portainer: Hacer clic en "Update the stack" o "Pull and redeploy".

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Bot de Telegram: `@DsctCDKeysPerubot`
- Repositorio Remoto: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- Archivo de filtros: `filters.py`
- Scraper de cupones: `scrapers/promo_feed_scraper.py`
