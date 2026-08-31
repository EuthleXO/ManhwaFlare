# ManhwaFlare — home panel
from telegram import InlineKeyboardMarkup
from Manhwaflare.config import (
    APP_VERSION, OWNER_USERNAME, OWNER_DISPLAY,
    SUPPORT_GROUP, SUPPORT_CHANNEL,
)
from Manhwaflare.text import sc
from Manhwaflare.ui.keyboards import btn, url_btn


def start_caption(user, is_owner: bool, plan_name: str = "Free", daily: str = "") -> str:
    name = (user.first_name if user else "user") or "user"
    daily_line = f"\n{sc('today')}: {daily}" if daily else ""
    return (
        f"<blockquote>"
        f"<b>{sc('welcome')} {name}</b>\n"
        f"{sc('your manhwa pdf companion')}"
        f"</blockquote>\n"
        f"<blockquote>"
        f"<b>{sc('plan')}:</b> {plan_name}{daily_line}\n"
        f"<b>{sc('version')}:</b> {APP_VERSION}"
        f"</blockquote>\n"
        f"<blockquote><b>{sc('tap a button below')}</b></blockquote>"
    )


def main_kb(is_owner: bool = False, is_admin: bool = False) -> InlineKeyboardMarkup:
    """Core home buttons + owner profile / support links."""
    # Owner profile URL buttons
    owner_row = []
    for o in OWNER_DISPLAY[:2]:
        un = (o.get("username") or "").lstrip("@")
        oid = o.get("id")
        label = un or str(oid) or "Owner"
        if un:
            owner_row.append(url_btn(f"@{label}", f"https://t.me/{un}"))
        elif oid:
            owner_row.append(url_btn(sc("owner"), f"tg://user?id={oid}"))
    if not owner_row:
        un = OWNER_USERNAME.lstrip("@") if OWNER_USERNAME else ""
        if un:
            owner_row.append(url_btn(f"@{un}", f"https://t.me/{un}"))

    ch = SUPPORT_CHANNEL.lstrip("@")
    grp = SUPPORT_GROUP
    if grp and not grp.startswith("http"):
        grp = f"https://t.me/{grp.lstrip('@')}"

    rows = [
        [
            btn(sc("search"), "p:search", "success"),
            btn(sc("trending"), "p:trending", "primary"),
        ],
        [
            btn(sc("help"), "p:help", "primary"),
            btn(sc("settings"), "p:settings", "primary"),
        ],
        [
            btn(sc("more"), "p:more", "success"),
        ],
    ]
    if owner_row:
        rows.append(owner_row)
    rows.append([
        url_btn(sc("support channel"), f"https://t.me/{ch}"),
        url_btn(sc("support group"), grp),
    ])
    if is_admin or is_owner:
        rows.append([btn(sc("admin"), "p:adminmenu", "danger")])
    return InlineKeyboardMarkup(rows)
