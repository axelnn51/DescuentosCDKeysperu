import urllib.request
import urllib.parse
import json
import time
import html
from typing import Optional, Tuple
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from models import Deal

class TelegramNotifier:
    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None):
        self.token = token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id and "TU_" not in self.token and len(self.token) > 15)

    def format_deal_caption(self, deal: Deal) -> str:
        clean_title = html.escape(deal.title)
        
        # Formato especial para promociones tipo 2x1 o Cupones
        if deal.deal_type in ("2x1", "coupon", "flash"):
            badge = "🎁 <b>¡PROMOCIÓN ESPECIAL / 2x1!</b> 🎁" if deal.deal_type == "2x1" else "🎟️ <b>¡CUPÓN EN VIVO DETECTADO!</b> 🎟️"
            caption = (
                f"{badge}\n\n"
                f"🏷️ <b>{clean_title}</b>\n\n"
                f"🏬 <b>Fuente:</b> {deal.store}\n"
            )
            if deal.discount_price > 0:
                caption += f"💰 <b>Precio:</b> <b>S/. {deal.discount_price:,.2f}</b>\n"
            caption += f"\n👉 <a href=\"{deal.url}\"><b>[ VER PROMOCIÓN / CANJEAR CUPÓN ]</b></a>"
            return caption

        # Formato para descuentos y liquidaciones directas
        caption = (
            f"🔥 <b>¡ALERTA DE REBAJA: {deal.discount_percent:.0f}% OFF!</b> 🔥\n\n"
            f"🛒 <b>{clean_title}</b>\n\n"
            f"🏬 <b>Tienda:</b> {deal.store}\n"
            f"💰 <b>Precio Oferta:</b> <b>S/. {deal.discount_price:,.2f}</b>\n"
            f"🏷️ <b>Precio Antes:</b> <s>S/. {deal.original_price:,.2f}</s>\n"
            f"💵 <b>Ahorras:</b> S/. {deal.savings:,.2f}\n"
        )
        if deal.stock > 0:
            caption += f"📦 <b>Stock disponible:</b> {deal.stock} unid.\n"
        
        caption += f"\n🔗 <a href=\"{deal.url}\"><b>[ VER OFERTA EN LA TIENDA ]</b></a>"
        return caption

    def send_deal(self, deal: Deal) -> bool:
        if not self.is_configured():
            print(f"[ALERTA LOCAL] {deal.store} | {deal.discount_percent}% OFF | S/. {deal.discount_price} (Antes: S/. {deal.original_price}) -> {deal.title}")
            return False

        caption = self.format_deal_caption(deal)

        # 1. Intentar enviar foto si hay URL de imagen disponible
        if deal.image_url:
            success = self._send_photo(deal.image_url, caption)
            if success:
                time.sleep(1.2)
                return True

        # 2. Si falla la foto o no tiene imagen, enviar mensaje de texto HTML
        success = self._send_message(caption)
        time.sleep(1.2)
        return success

    def _send_photo(self, photo_url: str, caption: str) -> bool:
        url = f"{self.base_url}/sendPhoto"
        payload = {
            "chat_id": self.chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("ok", False)
        except Exception:
            return False

    def _send_message(self, text: str) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("ok", False)
        except Exception as e:
            print(f"[ERROR TELEGRAM] {e}")
            return False

    def auto_detect_chat_id(self) -> Tuple[Optional[str], str]:
        """Consulta getUpdates para detectar el chat_id del último usuario que habló con el bot."""
        if not self.token:
            return None, "No hay TELEGRAM_BOT_TOKEN configurado."
        
        url = f"{self.base_url}/getUpdates"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("result", [])
                if not results:
                    return None, "Aún no se detectan mensajes. Por favor abre Telegram, busca a tu bot y dale a /start"
                
                last_update = results[-1]
                msg = last_update.get("message") or last_update.get("channel_post") or last_update.get("my_chat_member", {}).get("chat")
                if isinstance(msg, dict) and "chat" in msg:
                    chat = msg["chat"]
                elif isinstance(msg, dict) and "id" in msg:
                    chat = msg
                else:
                    return None, "No se pudo interpretar el tipo de chat en getUpdates."
                
                chat_id = str(chat.get("id"))
                chat_title = chat.get("title") or chat.get("username") or chat.get("first_name", "Desconocido")
                return chat_id, f"¡Chat detectado con éxito! Nombre: {chat_title} | ID: {chat_id}"
        except Exception as e:
            return None, f"Error al consultar getUpdates: {e}"

    def test_connection(self) -> Tuple[bool, str]:
        if not self.is_configured():
            return False, "Faltan credenciales: Por favor configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en las variables de entorno."
        
        test_text = (
            "🤖 <b>SPY DE REBAJAS PERÚ CONECTADO</b> 🇵🇪\n\n"
            "✅ La conexión con tu bot de Telegram es exitosa.\n"
            "🎯 Monitoreando rebajas con mínimo <b>75% de descuento</b> y cupones/promos activas."
        )
        ok = self._send_message(test_text)
        if ok:
            return True, "Mensaje de prueba enviado exitosamente a Telegram."
        else:
            return False, "No se pudo enviar el mensaje. Verifica que hayas iniciado chat con el bot en Telegram."
