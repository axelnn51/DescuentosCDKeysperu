# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-02 | Versión: v1.1.0 | Estado: Operativo & Dockerizado

## 1. 🚦 Estado Actual Inmediato
- 17 Tiendas y Marketplaces integrados: Plaza Vea, Metro, Wong, Oechsle, Promart, Coolbox, Footloose, Triathlon, Casaideas, Sony Store, Shopstar, La Curacao, Tiendas Efe, Hiraoka, Juntoz, Ripley y Falabella.
- Token de Telegram del bot `@DsctCDKeysPerubot` configurado (`1234567890:...`).
- Soporte Dockerfile & docker-compose.yml con volumen persistente en `/app/data` para despliegue directo en Portainer Stacks.
- Detección automática de chat ID vía `python spy.py --get-chat-id`.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **VTEX HTTP 206 Partial Content**: Manejado para Shopstar, Plaza Vea, Oechsle, Promart, etc.
- **Tiendas Magento 2 (La Curacao, Efe, Hiraoka)**: Implementado `MagentoScraper` con parseo de `.product-item-info`, `.old-price` y `.special-price`.
- **Juntoz (Next.js/Tailwind SPA)**: Implementado `JuntozScraper` extrayendo tarjetas `/p/` y precios `S/. X`.
- **Persistencia en Docker / Portainer**: La base SQLite reside en `data/deals.db` mapeada al volumen `/app/data`.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Mercado Libre API pública no autenticada**: Bloqueada con 403 por nuevo sistema OAuth estricto; no usar llamadas directas sin token OAuth.

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [x] Push a GitHub: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- [ ] Iniciar chat con `@DsctCDKeysPerubot` en Telegram y correr `python spy.py --get-chat-id` (o colocar el chat_id en Portainer).
- [ ] Desplegar Stack en Portainer.

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Bot de Telegram: `@DsctCDKeysPerubot`
- Repositorio Remoto: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- Configuración: `.env` / `docker-compose.yml`
