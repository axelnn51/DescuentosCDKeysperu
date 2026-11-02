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
                time.sleep(1.0) # Rate limiting respetuoso
                return True

        # 2. Si falla la foto o no tiene imagen, enviar mensaje de texto HTML
        success = self._send_message(caption)
        time.sleep(1.0)
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

    def test_connection(self) -> Tuple[bool, str]:
        if not self.is_configured():
            return False, "Faltan credenciales: Por favor configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en el archivo .env"
        
        test_text = (
            "🤖 <b>SPY DE REBAJAS PERÚ CONECTADO</b> 🇵🇪\n\n"
            "✅ La conexión con tu bot de Telegram es exitosa.\n"
            "🎯 Monitoreando rebajas con mínimo <b>75% de descuento</b>."
        )
        ok = self._send_message(test_text)
        if ok:
            return True, "Mensaje de prueba enviado exitosamente a Telegram."
        else:
            return False, "No se pudo enviar el mensaje. Verifica que el bot_token sea correcto y que hayas iniciado chat con el bot."
