# 📍 ACTIVE_CONTEXT: Spy de Rebajas Perú (Telegram Bot)
> Última Actualización: 2026-11-02 | Versión: v1.0.0 | Estado: Operativo (Listo para vincular Telegram)

## 1. 🚦 Estado Actual Inmediato
- Sistema de escaneo multi-tienda funcionando con detección en vivo de ofertas con mínimo 75% de descuento (hasta 99% OFF).
- Motor de alertas Telegram con formateo HTML, soporte para envío de fotos del producto, prevención de duplicados vía SQLite y control de tasa (rate limiting).
- Tiendas integradas y probadas en vivo: Plaza Vea, Metro, Wong, Oechsle, Promart, Coolbox, Footloose, Triathlon Sport, Casaideas, Sony Store, Ripley y Falabella.
- Comandos de ejecución:
  - `python spy.py --dry-run` : Escaneo de prueba en consola sin enviar a Telegram.
  - `python spy.py --scan-once` : Escaneo en vivo y envío directo a Telegram.
  - `python spy.py --daemon` : Monitoreo continuo 24/7 cada X minutos.
  - `python spy.py --test-telegram` : Prueba de conexión con el bot de Telegram.

## 2. 🧠 Base de Conocimiento de Errores (Caminos Resueltos vs Descartados)
### ✅ Errores Resueltos Definitivamente (No volver a diagnosticar)
- **VTEX HTTP 206 Partial Content**: Las consultas por rango de VTEX devuelven código 206 en lugar de 200. Manejado aceptando códigos 200 y 206.
- **Compresión GZIP en Sony Store**: Sony devuelve respuestas comprimidas `gzip`. Manejado con descompresión transparente de `gzip`.
- **UnicodeEncodeError en Windows (cp1252)**: PowerShell en Windows falla al imprimir caracteres UTF-8 como emojis. Resuelto configurando `sys.stdout.reconfigure(encoding="utf-8")`.
- **Deduplicación de ofertas**: Previene spam repetitivo en Telegram guardando cada oferta en `deals.db` (SQLite) y solo re-notificando si el precio baja aún más.

### ❌ Caminos Técnicos Fallidos / Descartados (Prohibido reintentar)
- **Llamadas estándar con `requests` a Falabella/Ripley**: Bloqueadas con 403 por protecciones Cloudflare/TLS fingerprinting. Descartado `requests` puro; se utiliza `curl_cffi` con impersonación de Chrome (`chrome124`) y extracción de `__NEXT_DATA__`.

## 3. 📋 Tareas Pendientes y Roadmap Inmediato
- [ ] Configurar `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en `.env` por parte del usuario.
- [ ] Opcional: Configurar tarea programada en Windows Task Scheduler o servicio para ejecución continua si se desea.

## 4. 🔗 Referencias Rápidas y Credenciales/Variables
- Archivo de configuración: `.env` (creado a partir de `.env.example`).
- Base de datos local de deduplicación: `deals.db` (SQLite).
- Punto de entrada principal: `spy.py`.
