# 🇵🇪 SPY DE REBAJAS PERÚ - BOT DE TELEGRAM (>= 75% OFF)

Un rastreador automatizado de ofertas y liquidaciones extremas en las principales tiendas y marketplaces de Perú. Monitorea continuamente las plataformas y despacha alertas instantáneas con foto, porcentaje de rebaja, precio de oferta, precio anterior y botón directo a tu bot o canal de Telegram.

---

## 🏬 Tiendas y Marketplaces Soportados

1. **Plaza Vea** (`plazavea.com.pe`) - Supermercado, tecnología, hogar.
2. **Metro** (`metro.pe`) - Supermercado, electrodomésticos, hogar.
3. **Wong** (`wong.pe`) - Gourmet, licores, tecnología.
4. **Oechsle** (`oechsle.pe`) - Tienda por departamento, moda, tecnología.
5. **Shopstar** (`shopstar.pe`) - Marketplace Intercorp.
6. **Promart** (`promart.pe`) - Mejoramiento del hogar, iluminación, herramientas.
7. **Coolbox** (`coolbox.pe`) - Tecnología, audio, accesorios móviles.
8. **La Curacao** (`lacuracao.pe`) - Electrodomésticos, cómputo, motos.
9. **Tiendas Efe** (`efe.com.pe`) - Electro, cómputo, televisores.
10. **Hiraoka** (`hiraoka.com.pe`) - Especialistas en tecnología y línea blanca.
11. **Juntoz** (`juntoz.com`) - Marketplace omnicanal.
12. **Footloose** (`footloose.pe`) - Calzado urbano y deportivo.
13. **Triathlon Sport** (`triathlon.com.pe`) - Calzado y moda deportiva.
14. **Casaideas** (`casaideas.com.pe`) - Hogar, organización, deco.
15. **Sony Store Perú** (`store.sony.com.pe`) - PlayStation, cámaras, audio.
16. **Ripley** (`simple.ripley.com.pe`) - Tienda por departamento.
17. **Falabella** (`falabella.com.pe`) - Tienda por departamento.

---

## 🚀 Inicio Rápido (En 3 Pasos)

### 1. Activar tu Bot en Telegram
1. Abre Telegram y busca a tu bot: **`@DsctCDKeysPerubot`**.
2. Dale al botón **Iniciar** o envíale `/start`.
3. Para obtener tu `chat_id` automáticamente, corre:
   ```bash
   python spy.py --get-chat-id
   ```
   *(Este comando detecta tu usuario y guarda tu `TELEGRAM_CHAT_ID` en el archivo `.env` por ti).*

### 2. Verificar Conexión
```bash
python spy.py --test-telegram
```

### 3. Ejecutar
* **Escanear una vez y enviar ofertas a Telegram:**
  ```bash
  python spy.py --scan-once
  ```
* **Modo Demonio (Monitoreo continuo 24/7):**
  ```bash
  python spy.py --daemon
  ```
* **Simulación en consola (sin enviar a Telegram):**
  ```bash
  python spy.py --dry-run
  ```

---

## 🐳 Despliegue en Portainer / Docker

Este proyecto está 100% preparado para desplegarse como un **Stack de Portainer**:

### Opción A: Desplegar desde Repositorio Git en Portainer
1. En tu panel de **Portainer**, ve a **Stacks** -> **Add stack**.
2. Selecciona el método **Repository**.
3. **Repository URL**: `https://github.com/axelnn51/DescuentosCDKeysperu.git`
4. **Repository reference**: `refs/heads/main`
5. **Compose path**: `docker-compose.yml`
6. En la sección **Environment variables** (Variables de entorno de Portainer), define:
   * `TELEGRAM_BOT_TOKEN`: `(tu_token_de_botfather_aqui)`
   * `TELEGRAM_CHAT_ID`: `(tu_chat_id_aqui)`
   * `MIN_DISCOUNT_PERCENT`: `50`
   * `SCAN_INTERVAL_MINUTES`: `15`
7. Clic en **Deploy the stack**. ¡Listo! El contenedor correrá en segundo plano vigilando las ofertas 24/7.

### Opción B: Ejecución local con Docker Compose
```bash
docker compose up -d --build
```
Para ver los logs en vivo:
```bash
docker compose logs -f
```

---

## 🛡️ Deduplicación Anti-Spam
El bot cuenta con persistencia SQLite (`data/deals.db`):
* Evita notificaciones repetidas de ofertas ya vistas.
* Solo re-notifica un producto si su precio baja aún más de lo reportado previamente.
