import os
from pathlib import Path

# Cargar variables de entorno manualmente o con dotenv si existe
ENV_PATH = Path(__file__).resolve().parent / ".env"

def load_dotenv_simple(env_file):
    if not os.path.exists(env_file):
        return
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v

load_dotenv_simple(ENV_PATH)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

try:
    MIN_DISCOUNT_PERCENT = float(os.getenv("MIN_DISCOUNT_PERCENT", "60"))
except ValueError:
    MIN_DISCOUNT_PERCENT = 60.0

try:
    SCAN_INTERVAL_MINUTES = int(os.getenv("SCAN_INTERVAL_MINUTES", "15"))
except ValueError:
    SCAN_INTERVAL_MINUTES = 15

try:
    MAX_ITEMS_PER_STORE = int(os.getenv("MAX_ITEMS_PER_STORE", "50"))
except ValueError:
    MAX_ITEMS_PER_STORE = 50

ENABLED_STORES = [s.strip().lower() for s in os.getenv("ENABLED_STORES", "").split(",") if s.strip()]
if not ENABLED_STORES:
    ENABLED_STORES = [
        "plazavea", "oechsle", "metro", "wong", "promart",
        "coolbox", "footloose", "triathlon", "casaideas", "sony",
        "shopstar", "lacuracao", "efe", "hiraoka", "juntoz",
        "ripley", "falabella", "knasta"
    ]

# Ruta de base de datos persistente (compatible con Docker / Portainer y Local)
DATA_DIR = Path("/app/data") if Path("/app/data").is_dir() else (Path(__file__).resolve().parent / "data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "deals.db"
