# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-02 | Versión: v1.3.0 | Estado: Operativo, Mínimos Históricos & Fuentes Originales

## 1. 🚦 Estado Actual Inmediato
- 18 Fuentes Oficiales y Directas de Tiendas en Perú (Plaza Vea, Oechsle, Metro, Wong, Promart, Coolbox, Footloose, Triathlon, Casaideas, Sony, Shopstar, La Curacao, Efe, Hiraoka, Juntoz, Ripley, Falabella).
- Integración del motor de precios históricos de **Knasta Perú** (`scrapers/knasta_scraper.py`): detecta cuándo un producto toca su **Mínimo Histórico Real** en tiendas peruanas.
- Eliminado completamente cualquier raspado de canales de Telegram de terceros (cero copias, 100% fuentes directas a tiendas oficiales).
- Filtro inteligente anti-chatarra y detector de precios inflados activo.
- Cupo ampliado a **15 ofertas TOP por ciclo** con priorización de Mínimos Históricos y mayor ahorro en Soles.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **Feeds de terceros descartados**: Eliminado `promo_feed_scraper.py`. Toda la data proviene exclusivamente de tiendas originales y comparadores oficiales de precios peruanos.
- **Pocas ofertas / Umbral muy rígido**: Ajustado `MIN_DISCOUNT_PERCENT` a 60% por defecto (y caídas del 20-35% si es Mínimo Histórico en tecnología/electro), aumentando a 15 las alertas por ciclo.
- **Portainer "env file .env not found"**: Resuelto eliminando `env_file` y usando variables directas en `docker-compose.yml`.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Scrapear canales de Telegram de ofertas**: Descartado por petición expresa del usuario (evitar contenido duplicado/no original).

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [x] Push a GitHub: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- [ ] En Portainer: Hacer clic en "Pull and redeploy".

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Bot de Telegram: `@DsctCDKeysPerubot`
- Repositorio: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- Motor de Mínimos Históricos: `scrapers/knasta_scraper.py`
