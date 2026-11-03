# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot + Portainer)
> Última Actualización: 2026-11-03 | Versión: v1.4.1 | Estado: Seguridad Sanitizada (Cero Secretos) & Portainer Configurado

## 1. 🚦 Estado Actual Inmediato
- **Seguridad y Cero Secretos**: Token de Telegram purgado completamente de todo el historial de Git (`git-filter-repo`). Forzado `push origin main --force`. GitGuardian resuelto.
- **Inyección por Portainer**: `docker-compose.yml` ahora lee `${TELEGRAM_BOT_TOKEN}` y `${TELEGRAM_CHAT_ID}` directo de las *Environment Variables* de Portainer, sin valores por defecto expuestos.
- **Filtros y Balance Multi-Tienda (v1.4.0)**: Scoring ponderado de dinero real ahorrado, detector de precios inflados por sellers y balance de máximo 3 ofertas por tienda por ciclo (15 por ciclo).
- `.gitignore` blindado para ignorar cualquier `.env` o credencial.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **Fuga de Token en Git / GitGuardian**: Eliminado de todos los commits históricos y del código actual. Sustituido por variables de entorno de Portainer.
- **Precios inflados de sellers (ej: Oster a S/. 16,990 o ViewSonic a S/. 10,089)**: Resuelto con topes categóricos plausibles en `filters.py`.
- **Mínimos Históricos insignificantes (0-2%)**: Knasta exige al menos 20-25% y S/. 100 de ahorro real.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Hardcodear tokens o IDs en compose o README**: Descartado por seguridad. Siempre usar variables en Portainer.

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [x] Purgar secretos del historial de Git y subir a GitHub con `--force`.
- [ ] En Telegram: Enviar `/revoke` a `@BotFather` para generar un nuevo token seguro (recomendado por alerta de GitGuardian).
- [ ] En Portainer: En el Stack `descuentos`, definir las variables de entorno `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` y hacer clic en **"Update the stack"** / **"Pull and redeploy"**.

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Bot de Telegram: `@DsctCDKeysPerubot`
- Repositorio: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
- Variables en Portainer: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MIN_DISCOUNT_PERCENT=50`
