# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-02 | Versión: v1.1.0 | Estado: Operativo & Dockerizado

## 1. 🚦 Estado Actual Inmediato
- 17 Tiendas y Marketplaces integrados y operativos.
- Token de Telegram del bot `@DsctCDKeysPerubot` configurado (`1234567890:...`).
- Código subido y sincronizado con GitHub en `main` (`https://github.com/axelnn51/DescuentosCDKeysperu.git`).
- Soporte Dockerfile & docker-compose.yml listo para desplegar en Portainer Stacks sin error de repositorio vacío.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **Portainer "env file .env not found"**: Portainer no clona archivos ignorados por git (.env). Solucionado eliminando `env_file: - .env` y pasando variables directas con valores por defecto en `docker-compose.yml`.
- **Portainer "remote repository is empty"**: El repositorio en GitHub aún no había recibido el primer push. Resuelto configurando el origen con usuario explícito `axelnn51@github.com` y ejecutando el push a `main`.
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
