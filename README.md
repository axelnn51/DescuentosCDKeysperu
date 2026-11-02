# 🇵🇪 SPY DE REBAJAS PERÚ - BOT DE TELEGRAM (>= 75% OFF)

Un rastreador automatizado de ofertas y liquidaciones masivas en los principales e-commerce y tiendas por departamento de Perú (Plaza Vea, Metro, Wong, Oechsle, Promart, Coolbox, Footloose, Triathlon, Casaideas, Sony Store, Ripley y Falabella).

Filtra exclusivamente productos con **mínimo 75% de descuento** (con descuentos de hasta 99% OFF) y los envía instantáneamente con foto, precio original, precio oferta, porcentaje de ahorro y enlace directo a tu bot o canal de Telegram.

---

## 🚀 Inicio Rápido (En 3 Pasos)

### 1. Configurar tu Bot de Telegram
1. Abre Telegram y busca a **[@BotFather](https://t.me/BotFather)**.
2. Envía `/newbot`, dale un nombre y un usuario a tu bot (terminado en `bot`).
3. Copia el **HTTP API Token** que te entregará (ejemplo: `7123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
4. Para obtener tu `chat_id`:
   - Si es para ti en privado: Escríbele cualquier mensaje a **[@userinfobot](https://t.me/userinfobot)** y copia tu `Id`.
   - Si es para un **Canal o Grupo**: Agrega a tu bot como Administrador del canal/grupo y usa el `@nombre_del_canal` (ej: `@mis_rebajas_peru`) o el ID numérico del grupo.

### 2. Guardar credenciales en `.env`
Abre el archivo `.env` en la raíz de este proyecto y coloca tu token y chat ID:

```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
MIN_DISCOUNT_PERCENT=75
```

### 3. Verificar conexión y ejecutar
Prueba que tu bot esté conectado:
```bash
python spy.py --test-telegram
```

Ejecuta el primer escaneo de ofertas:
```bash
python spy.py --scan-once
```

---

## 🛠️ Modos de Ejecución

| Comando | Descripción |
|---|---|
| `python spy.py --dry-run` | Busca ofertas >= 75% y las muestra en la consola sin enviarlas a Telegram (ideal para pruebas). |
| `python spy.py --scan-once` | Realiza un escaneo completo de todas las tiendas y envía las nuevas ofertas a Telegram. |
| `python spy.py --daemon` | Monitoreo continuo 24/7 en segundo plano (escanea cada 15 minutos automáticamente). |
| `python spy.py --store oechsle` | Escanea únicamente una tienda en específico. |
| `python spy.py --min-discount 80` | Ajusta temporalmente el porcentaje de descuento mínimo a 80%. |
| `python spy.py --stats` | Muestra el resumen de ofertas registradas en la base de datos local. |

---

## 🏬 Tiendas Soportadas

- **Plaza Vea** (Supermercado, tecnología, hogar)
- **Metro** (Supermercado, electrodomésticos, hogar)
- **Wong** (Supermercado, licores, tecnología)
- **Oechsle** (Tienda por departamento, moda, tecnología, belleza)
- **Promart** (Mejoramiento del hogar, iluminación, herramientas)
- **Coolbox** (Tecnología, audio, accesorios móviles, gadgets)
- **Footloose** (Calzado urbano y deportivo)
- **Triathlon Sport** (Ropa deportiva y zapatillas de marca)
- **Casaideas** (Hogar, decoración, cocina)
- **Sony Store Perú** (PlayStation, audio, cámaras, TVs)
- **Ripley** (Tienda por departamento)
- **Falabella** (Tienda por departamento)

---

## 🛡️ Anti-Spam y Base de Datos Local
El sistema incluye una base de datos local SQLite (`deals.db`) que:
- Registra cada oferta enviada.
- Evita notificaciones repetidas del mismo producto.
- Solo vuelve a notificar un producto si su precio baja aún más de lo reportado previamente.
