# © ManhwaFlare — @flexyy | dragonByte | @dragonByte_Network
# Do not remove credits
"""ManhwaFlare Bot — config"""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Primary owner from env + fixed co-owner
_env_owner = int(os.getenv("OWNER_ID", "0") or 0)
_FIXED_OWNER = 8681820826  # always owner
_extra = os.getenv("OWNER_IDS", "").strip()  # comma-separated optional
OWNER_IDS = set()
if _env_owner:
    OWNER_IDS.add(_env_owner)
OWNER_IDS.add(_FIXED_OWNER)
if _extra:
    for part in _extra.split(","):
        part = part.strip()
        if part.isdigit():
            OWNER_IDS.add(int(part))

# Back-compat single OWNER_ID (first preferred env, else fixed)
OWNER_ID = _env_owner or _FIXED_OWNER

OWNER_USERNAME = os.getenv("OWNER_USERNAME", "flexyy").lstrip("@")
# Display owners on home / premium contact
OWNER_DISPLAY = [
    {"id": _FIXED_OWNER, "username": "flexyy", "label": "Owner"},
]
if _env_owner and _env_owner != _FIXED_OWNER:
    OWNER_DISPLAY.insert(0, {"id": _env_owner, "username": OWNER_USERNAME, "label": "Owner"})

SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/+CZCfHr3AHKUwNTJk").strip()
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "DragonByte_network").lstrip("@")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "-1003915347751") or -1003915347751)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017").strip()
DATABASE_NAME = os.getenv("DATABASE_NAME", "manhwaflare").strip()
SCRAPE_HOST = os.getenv("SCRAPE_HOST", "https://manhwa18.net").rstrip("/")
SCRAPE_HOST_NET = os.getenv("SCRAPE_HOST_NET", "https://manhwa18.net").rstrip("/")
SCRAPE_SOURCE = os.getenv("SCRAPE_SOURCE", "net")
CAPTION_TAG = os.getenv("CAPTION_TAG", "").strip()
FILENAME_TEMPLATE = os.getenv("FILENAME_TEMPLATE", "{chapter_num} ⌯ {manga_title} [{tag}]")
PORT = int(os.getenv("PORT", "8080"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
UPSTREAM_REPO = "https://github.com/EuthleXO/ManhwaFlare.git"
REPO_URL = "https://github.com/EuthleXO/ManhwaFlare"
APP_VERSION = "v3.1"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, "tmp")
os.makedirs(TMP_DIR, exist_ok=True)
MAX_CONCURRENT = 3
UPLOAD_RATE = 15
PAGE_SIZE = 8

START_IMAGES = [
    "https://i.postimg.cc/PrNm8t2G/03ee94efd955d189e970a5de76a9000f.jpg",
    "https://i.postimg.cc/c46Q8sXG/0bc8ecc0951cf0c579b769f9c71fef03.jpg",
    "https://i.postimg.cc/NfL1rgbd/21ce8df86f292cb7fc56c6b7cab6242c.jpg",
    "https://i.postimg.cc/m2hQFbVS/257d6870ee2c467468d25cdd313e7df0.jpg",
    "https://i.postimg.cc/L6hzZHNM/26f186c1de6f80d124942d715ff7a846.jpg",
]

COPYRIGHT = ""  # not shown in UI
